import collections
import itertools
import os
import sys
import threading
import time
from multiprocessing import Process, Lock, Queue

import urwid


class ChoiceSelector(urwid.Padding):
    main = None

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose ', choice, u'\n'])
        done = urwid.Button(u'Ok')
        urwid.connect_signal(done, 'click', self.exit_program)
        self.main.original_widget = urwid.Filler(urwid.Pile([response,
                                                             urwid.AttrMap(done, None,
                                                                           focus_map='normal')]))

    def __init__(self):
        super().__init__(urwid.ListBox(urwid.SimpleFocusListWalker([])))

    def generate_choices(self, title, choices):
        self.main = urwid.Padding(
            self.menu(title, choices),
            left=2, right=2
        )

    def menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', self.item_chosen, c)
            body.append(urwid.AttrMap(button, None, focus_map='normal'))
        # ok_button = urwid.Button('OK')
        # urwid.connect_signal(ok_button, 'click', self.item_chosen, c)
        # body.append(urwid.AttrMap(ok_button, None, focus_map='normal'))  # ?
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def clear(self):
        pass


class DownloadBox(urwid.ListBox):
    pids = collections.defaultdict(lambda: urwid.Text(''))
    downloads = urwid.SimpleListWalker([])

    def __init__(self):
        super().__init__(
            self.downloads
        )

    # TODO: Add meaningful docstrings to explain this retardness (cleverness)
    def update(self, pid, line):
        self.pids[pid].set_text(line)
        self.update_downloads()

    def delete(self, pid):
        del self.pids[pid]
        self.update_downloads()

    def update_downloads(self):
        self.downloads[:] = self.intersperse(
            lst=list(self.pids.values()),
            delimiter=urwid.Divider()
        )

    @staticmethod
    def intersperse(lst, delimiter):
        """
        Add delimiter object between each item in the list.
        Args:
            lst (list): List of objects you want to separate.
            delimiter: Delimiter object.

        Returns:
            list: List of separated objects.

        """
        result = [delimiter] * (len(lst) * 2 - 1)
        result[0::2] = lst
        return result


class BodyView(urwid.Pile):
    def __init__(self):
        self.download_box = DownloadBox()
        self.choice_menu = ChoiceSelector()
    # self.choice_menu = urwid.BoxAdapter(urwid.AttrWrap(ChoiceSelector(), 'reversed'), height=8)

        self.elements = [
            self.download_box,
            urwid.AttrWrap(self.choice_menu, 'reversed')
        ]
        super().__init__(self.elements)

    def change_text_block(self, index, text):
        self.download_box.update(index, text)

    def delete_text_block(self, index):
        self.download_box.delete(index)


class TerminalUI:
    """
    Simple terminal UI with header, footer and body containing:
        a) information about videos being downloaded
        b) choice menu for new videos.
    Initialize with your TerminalUI instance to execute commands and then
    start main loop TerminalUI.loop().
    Output download information from other other processes with
    TerminalUI.update_block(pid, text)
    """

    PALLETE = [('reversed', urwid.BLACK, urwid.LIGHT_GRAY),
               ('normal', urwid.LIGHT_GRAY, urwid.BLACK),
               ('error', urwid.LIGHT_RED, urwid.BLACK),
               ('green', urwid.DARK_GREEN, urwid.BLACK),
               ('blue', urwid.LIGHT_BLUE, urwid.BLACK),
               ('magenta', urwid.DARK_MAGENTA, urwid.BLACK), ]

    def __init__(self, title, queue):
        self.queue = queue

        self._output_styles = [s[0] for s in self.PALLETE]
        self._eloop_thread = None
        self.eloop = None

        self.header = urwid.Text(title)
        self.body = BodyView()
        self.footer = urwid.Text('Footer')

        self.frame = urwid.Frame(
            body=urwid.AttrWrap(self.body, 'normal'),
            header=urwid.AttrWrap(self.header, 'reversed'),
            footer=urwid.AttrWrap(self.footer, 'normal'),
            focus_part='body'
        )

        # self.set_focus_path(['footer', 1])
        # self._focus = True
        # urwid.connect_signal(self.input,'line_entered',self.on_line_entered)

    def loop(self, handle_mouse=False):
        main = urwid.Overlay(self.frame, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
                             align='center', width=('relative', 95),
                             valign='middle', height=('relative', 95),
                             min_width=20, min_height=9)
        self.eloop = urwid.MainLoop(main,
                                    self.PALLETE,
                                    # unhandled_input=self.unhandled_input,
                                    handle_mouse=handle_mouse)
        self._eloop_thread = threading.current_thread()
        self.livereload_downloads()
        self.eloop.run()

    def unhandled_input(self, k):
        if k == 'esc':
            raise urwid.ExitMainLoop()

    def refresh_screen(self):
        if self.eloop and self._eloop_thread != threading.current_thread():
            self.eloop.draw_screen()

# TODO: move to DownloadBox class and start thread in __init__ method?
######################################################################
    def update_block(self, pid, line, style=None):
        if style and style in self._output_styles:
            line = (style, line)
        self.body.change_text_block(pid, line)
        self.refresh_screen()

    def delete_block(self, pid):
        self.body.delete_text_block(pid)
        self.refresh_screen()

    def livereload_downloads(self):
        def livereload():
            while True:
                pid, msg = self.queue.get()

                if isinstance(msg, str):
                    self.update_block(pid, msg, 'green')
                elif isinstance(msg, TerminateBlock):
                    self.delete_block(pid)
                else:
                    continue

        t = threading.Thread(target=livereload)
        t.daemon = True
        t.start()
######################################################################

    # def _update_focus(self, focus):
    #     self._focus=focus

    # def switch_focus(self):
    #     if self._focus:
    #         self.set_focus('body')
    #         self._focus=False
    #     else:
    #         self.set_focus_path(['footer',1])
    #         self._focus=True

    # def keypress(self, size, key):
    #     if key=='tab':
    #         self.switch_focus()
    #     return urwid.Frame.keypress(self, size, key)


class TerminateBlock:
    pass


class PrintCapturer:
    queue = None
    text = ''

    def __init__(self, queue):
        self.queue = queue

    def write(self, message):
        self.merge_message(message)
        self.queue.put((self.process_id, self.text))

    def merge_message(self, message):
        message_lines_list = []

        self.text += message
        lines = self.text.split('\n')

        for line in lines:
            message_lines_list.append(line.split('\r')[-1])

        self.text = '\n'.join(message_lines_list)

    def flush(self):
        pass

    def terminate(self):
        term = TerminateBlock()
        self.queue.put((self.process_id, term))

    @property
    def process_id(self):
        return os.getpid()


class Printer:
    output = collections.defaultdict(str)
    lines_count = None
    delimiter = None

    ERASE_LINE = '\x1b[2K'
    # """
    # Erases the screen from the current line down to the bottom of the
    # screen.
    # """
    # self.write_raw('\x1b[J')
    # TODO: use erase screen instead of erase n lines

    CURSOR_UP_ONE = '\x1b[1A'
    CURSOR_BEGINNING = '\033[1G'

    def __init__(self, commander, delimiter='-'):
        self.lines_count = 0
        self.delimiter = delimiter * 10
        self.commander = commander

        self.lock = Lock()

        # only linux
        # rows, columns = map(int, os.popen('stty size', 'r').read().split())
        # self.rows, self.columns = rows, columns
        # self.delimiter = delimiter * int(self.columns)

    def count_output_lines(self, out: dict) -> int:
        lines = 0
        # TODO: change item name rofl
        for key, text_block in out.items():
            lines += len(text_block.split('\n'))

        if self.delimiter:
            lines += len(out) - 1
        return lines

    def merge_message(self, pid, message):
        message_lines_list = []

        self.output[pid] += message
        lines = self.output[pid].split('\n')

        for line in lines:
            message_lines_list.append(line.split('\r')[-1])

        self.output[pid] = '\n'.join(message_lines_list)

    def write(self, entry: dict):
        if not entry.get('message'):
            return None

        pid = entry['process_id']
        message = entry['message']

        self.lock.acquire()

        self.merge_message(pid, message)
        self.clear_previous_output()

        out = self.output.copy()
        self.lines_count = self.count_output_lines(out)

        self.print_output(out)

        self.lock.release()

    # TODO: lock on all sys.__stdout__.write() and flush() ??
    def print_output(self, out: dict):
        # TODO: change to_print to more meaningful name
        to_print = f'\n{self.delimiter}\n'.join(out.values())
        sys.__stdout__.write(to_print)

    def erase_line(self):
        sys.__stdout__.write(self.ERASE_LINE)

    def move_cursor_up_one(self):
        sys.__stdout__.write(self.CURSOR_UP_ONE)

    def move_cursor_begin_line(self):
        sys.__stdout__.write(self.CURSOR_BEGINNING)

    def clear_previous_output(self):
        self.erase_line()
        for _ in range(self.lines_count - 1):
            self.move_cursor_up_one()
            self.erase_line()
        self.move_cursor_begin_line()

    def terminate(self, process_id):
        del self.output[process_id]

    def flush(self):
        self.lock.acquire()
        sys.__stdout__.flush()
        self.lock.release()


class collect_stdout:
    def __init__(self, queue):
        self.capturer = PrintCapturer(queue)

    def __enter__(self):
        self.save_stdout = sys.stdout
        sys.stdout = self.capturer

    def __exit__(self, *args):
        sys.stdout = self.save_stdout
        self.capturer.terminate()


def run(queue, start, step):
    with collect_stdout(queue):
        for i in itertools.count(start, step):
            print(f'Kappa, {i}', file=sys.stdout)
            time.sleep(1)
            if i >= 3000:
                break


if __name__ == '__main__':
    q = Queue()
    ui = TerminalUI('RTV video downloader', q)

    t1 = Process(target=run, args=(q, 500, 600))
    t1.daemon = True
    t1.start()
    t2 = Process(target=run, args=(q, 1500, 500))
    t2.daemon = True
    t2.start()

    ui.loop()
