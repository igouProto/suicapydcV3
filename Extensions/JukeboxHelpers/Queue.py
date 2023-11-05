import wavelink
from .Errors import *
class Queue(wavelink.Queue):
    def __init__(self):
        super().__init__()

        self.repeated_times = 0
        self.repeat_one_flag = False
        self.repeat_all_flag = False

    