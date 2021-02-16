import time
import threading as th
from collections import namedtuple


def q(n, word):
    if n != 1:
        word += "s"
    return f"{n} {word}"


class Delayer:
    def __init__(self, max_bulk_size, delay_seconds):
        self.lock = th.Lock()
        self.bulk_size = 0
        self.max_bulk_size = max_bulk_size
        self.delay_seconds = delay_seconds

    def __enter__(self):
        with self.lock:
            self.bulk_size += 1

            if self.bulk_size >= self.max_bulk_size:
                time.sleep(self.delay_seconds)
                self.bulk_size = 0

    def __exit__(self, *args, **kwargs):
        pass


PseudoUser = namedtuple("PseudoUser", ["telegram_id"])
