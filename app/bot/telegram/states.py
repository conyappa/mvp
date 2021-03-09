from collections import defaultdict
from app.utils import Singleton


class Manager(metaclass=Singleton):
    def __init__(self):
        self.count = 0
        self.spaces = defaultdict(dict)

    def register(self, flow, state):
        self.spaces[flow][state] = self.count
        self.count += 1

    def __getitem__(self, keys):
        flow, state = keys
        return self.spaces[flow][state]


STATES = Manager()
