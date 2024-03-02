from typing import Any
import wavelink
from .Queue import Queue
from .Errors import *


class Player(wavelink.Player):
    """
    A custom player class that extends wavelink.Player
    Includes a custom queue class that extends wavelink.Queue and a bounded channel for sending system messages
    """

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.queue: Queue = Queue()
        self.bounded_channel = None

        # workaround to let go_back() working properly, see Queue.back() for details
        self.queue_was_empty = False

    async def teardown(self):
        try:
            await super().disconnect()
            # self.clear_state()
        except KeyError:
            pass

    # Queue management
    async def add(self, ctx, tracks):
        new_track = await self.queue.add(tracks)

        # play the song if the queue is empty or if the player is not playing
        if self.queue.is_empty or not self.playing:
            await self.play(self.queue.next)

        self.queue_was_empty = False

        return new_track

    # move to the next song. should be triggered when the current song ends
    async def advance(self):
        try:
            await self.play(self.queue.next)
        except QueueIsEmpty:
            self.queue_was_empty = True
            raise QueueIsEmpty
        except Exception as e:
            raise e

        # print("hist", self.queue.history)
        # print("current", self.current)
        # print("queue", self.queue)

        self.queue_was_empty = False

        # counting repeated times cuz i'm bored
        if self.queue.mode == wavelink.QueueMode.loop:
            self.queue.increment_loop_count()
        else:
            self.queue.reset_loop_count()

    # back to the previous song
    def go_back(self):
        try:
            self.queue.back(queue_was_empty=self.queue_was_empty)
        except QueueIsEmpty:
            raise QueueIsEmpty

    async def toggle_loop_one(self):
        self.queue.toggle_loop_one()

        return self.queue.is_looping_one

    async def toggle_loop_all(self):
        self.queue.toggle_loop_all()

        return self.queue.is_looping_all

    def shuffle(self):
        self.queue.shuffle()

    def clear(self):
        self.queue.clear()

    def clear_history(self):
        self.queue.history.clear()

    def get_paginated_queue(self, page: int | str):
        return self.queue.get_paginated_queue(page)

    def move_song_to_top(self, index: int):
        self.queue.top(index)

    def remove_song(self, index: int):
        return self.queue.rm(index)

    # def clear_state(self):
    #     self.queue.reset_state()

    # def toggle_auto_play(self):
    #     self.autoplay = not self.autoplay

    @property
    def is_looping_one(self):
        return self.queue.is_looping_one

    @property
    def is_looping_all(self):
        return self.queue.is_looping_all

    @property
    def loop_count(self):
        return self.queue.repeated_times
