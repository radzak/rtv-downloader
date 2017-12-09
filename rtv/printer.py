import collections
import contextlib
import os
import sys
import threading


class Printer:
    output = collections.defaultdict(str)
    lines_count = None
    rows = None
    columns = None
    delimiter = None

    ERASE_LINE = '\x1b[2K'
    CURSOR_UP_ONE = '\x1b[1F'

    def __init__(self, delimiter='-'):
        self.lines_count = 0
        rows, columns = map(int, os.popen('stty size', 'r').read().split())
        self.rows, self.columns = rows, columns
        self.delimiter = delimiter * int(self.columns)

    def count_output_lines(self, out: dict) -> int:
        lines = 0
        # TODO: change item name rofl
        for key, item in out.items():
            lines += len(item.split('\n'))

        if self.delimiter:
            lines += len(out) - 1
        return lines

    def write(self, *args, **kwargs):
        if not args[0]:
            return None

        thread_id = threading.get_ident()
        self.output[thread_id] += args[0]  # lock it?

        self.clear_previous_output()

        out = self.output.copy()
        self.lines_count = self.count_output_lines(out)

        self.print_output(out)

    def print_output(self, out: dict):
        # TODO: change to_print to more meaningful name
        to_print = f'\n{self.delimiter}\n'.join(out.values())
        sys.__stdout__.write(to_print)

    def erase_line(self):
        sys.__stdout__.write(self.ERASE_LINE)

    def move_cursor_up_one(self):
        sys.__stdout__.write(self.CURSOR_UP_ONE)

    def clear_previous_output(self):
        self.erase_line()
        for _ in range(self.lines_count - 1):
            self.move_cursor_up_one()
            self.erase_line()

    def terminate(self):
        thread_id = threading.get_ident()
        del self.output[thread_id]

    @staticmethod
    def flush():
        sys.__stdout__.flush()


@contextlib.contextmanager
def redirect_stdout():
    save_stdout = sys.stdout
    sys.stdout = Printer()
    yield
    sys.stdout = save_stdout
