import collections
import contextlib
import itertools
import os
import sys
import time
from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager


class PrintCapturer:
    def __init__(self, printer):
        self.printer = printer

    def write(self, message):
        entry = {
            'process_id': self.process_id,
            'message': message
        }
        self.printer.write(entry)

    def flush(self):
        self.printer.flush()

    def terminate(self):
        self.printer.terminate(self.process_id)

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

    def __init__(self, delimiter='-'):
        self.lines_count = 0
        self.delimiter = delimiter * 10
        self.lock = Lock()
        self.file = open('/home/jatimir/tmp/podcasts_test.txt', 'a')
        self.file.write('init printera')
        self.file.flush()

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


@contextlib.contextmanager
def collect_stdout(printer: Printer):
    save_stdout = sys.stdout
    sys.stdout = PrintCapturer(printer)
    yield
    sys.stdout.terminate()
    sys.stdout = save_stdout


def run(printer, start, step):
    with collect_stdout(printer):
        for i in itertools.count(start, step):
            print(f'Kappa, {i}', file=sys.stdout)
            time.sleep(1)
            if i >= 3000:
                break


def main():
    BaseManager.register('Printer', Printer)
    manager = BaseManager()
    manager.start()
    printer = manager.Printer()

    t1 = Process(target=run, args=(printer, 500, 600))
    t1.start()
    t2 = Process(target=run, args=(printer, 1500, 500))
    t2.start()

    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
