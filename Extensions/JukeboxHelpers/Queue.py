import wavelink
from .Errors import *


class Queue(wavelink.Queue):

    def __init__(self):
        super().__init__()

        self.repeated_times = 0
        self.songs_per_page = 10
        self.current_page = 1

    # playback and navigating
    async def add(self, tracks):
        """
        Adds tracks to the queue
        """
        if isinstance(tracks, wavelink.Playlist):
            self.put(tracks)
            new_track = tracks.tracks[0]
        else:
            self.put(tracks[0])
            new_track = tracks[0]

        return new_track

    # get the next song
    @property
    def next(self):
        """
        Gets the next song from the queue
        """
        if self.is_empty and (self.mode == wavelink.QueueMode.normal):
            raise QueueIsEmpty

        next_track = self.get()
        return next_track

    # going to the previous song
    def back(self):
        """
        Backs to the previous song.
        Dequeue twice from the history queue and enqueues them to the main queue.
        """
        try:
            for _ in range(2 if self.history.count > 1 else 1):
                self.put_at(0, self.history.get_at(-1))
        except QueueIsEmpty:
            raise QueueIsEmpty

    """
    Loop Controls
    """

    @property
    def is_looping_one(self):
        return self.mode == wavelink.QueueMode.loop

    @property
    def is_looping_all(self):
        return self.mode == wavelink.QueueMode.loop_all

    @property
    def loop_count(self):
        return self.repeated_times

    def increment_loop_count(self):
        self.repeated_times += 1

    def reset_loop_count(self):
        self.repeated_times = 0

    def toggle_loop_one(self):
        if self.mode == wavelink.QueueMode.loop:
            self.mode = wavelink.QueueMode.normal
        else:
            self.mode = wavelink.QueueMode.loop

    def toggle_loop_all(self):
        if self.mode == wavelink.QueueMode.loop_all:
            self.mode = wavelink.QueueMode.normal
        else:
            self.mode = wavelink.QueueMode.loop_all

    """
    Queue querying
    """

    def get_paginated_queue(self, page: int | str):
        """
        Returns a paginated list of songs in the queue.
        If no page number is provided, return the first page.
        If we got ">" or "<" instead of a number, skip pages according to the number of such symbols.
        """
        if not page or page == "":
            page = 1

        if isinstance(page, str):
            if ">" in page:
                page = self.current_page + page.count(">")
            elif "<" in page:
                page = self.current_page - page.count("<")

        # cap page between 1 and max page (ceil(count / songs per page))
        max_page = (self.count // self.songs_per_page) + 1
        page = max(min(page, max_page), 1)

        # update current page
        self.current_page = page

        # send paginated queue
        return (
            list(self._items)[
                (page - 1) * self.songs_per_page : page * self.songs_per_page
            ],
            page,
            max(max_page, 1),
        )

    """
    Queue manipulation
    """

    def rm(self, index) -> wavelink.Playable:
        """
        Removes a song from the current page the user's seeing
        """
        # raise error if index out of range
        if index < 1 or index > self.songs_per_page:
            raise IndexError

        # compute the true index with the # of the current page the user's seeing
        real_idx = (self.current_page - 1) * self.songs_per_page + (index - 1)

        # peek at the item to be removed cuz we want to return the info of it
        item_deleted = self.peek(real_idx)

        # then remove it
        self.delete(real_idx)

        return item_deleted

    # moving a song to the top of the queue
    def top(self, index) -> wavelink.Playable:
        """
        Raises a song from the page the user's seeing to the top of the queue
        """
        # raise error if index out of range
        if index < 1 or index > self.songs_per_page:
            raise IndexError

        # remove it, then put it back to the top of the queue
        item = self.rm(index)

        self.put_at(0, item)