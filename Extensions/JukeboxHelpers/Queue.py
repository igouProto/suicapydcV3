import wavelink
from .Errors import *

"""

"""

class Queue(wavelink.Queue):
    def __init__(self):
        super().__init__()

        self.repeated_times = 0
        self.songs_per_page = 10
        self.current_page = 1

    # properties
    @property
    def next(self):
        if self.is_empty and not (self.loop_all or self.loop):
            raise QueueIsEmpty

        next_track = self.get()
        return next_track

    @property
    def loop_count(self):
        return self.repeated_times

    @property
    def is_looping_one(self):
        return self.loop

    @property
    def is_looping_all(self):
        return self.loop_all

    # methods
    def increment_loop_count(self):
        self.repeated_times += 1

    def reset_loop_count(self):
        self.repeated_times = 0

    async def add(self, tracks):
        if isinstance(tracks, wavelink.YouTubePlaylist):
            self.put(tracks)
            new_track = tracks.tracks[0]
        else:
            self.put(tracks[0])
            new_track = tracks[0]

        return new_track

    def back(self):
        """
        Backs to the previous song.
        Dequeues twice from the history queue and enqueues them to the main queue.
        """
        try:
            for _ in range(2 if self.history.count > 1 else 1):
                self.put_at_front(self.history.pop())
        except IndexError or QueueIsEmpty:
            pass
        '''
        print("Queue.back(): Backed to the previous song")
        print("Next", self)
        print("Prev", self.history)
        '''
        # return
       

    def toggle_loop_one(self):
        if self.loop:
            self.loop = False
        else:
            self.loop = True
            self.loop_all = False

    def toggle_loop_all(self):
        if self.loop_all:
            self.loop_all = False
        else:
            self.loop_all = True
            self.loop = False

    # TODO: Consider showing the history queue as well. Combine both and paginate as one?
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
            list(self._queue)[
                (page - 1) * self.songs_per_page : page * self.songs_per_page
            ],
            page,
            max(max_page, 1),
        )

    def move_song_to_top(self, index: int):
        """
        Moves a song to the top of the queue.
        """
        # raise error if index is out of range
        if index < 1 or index > self.songs_per_page:
            raise IndexError
        
        # compute index with the current page and songs per page
        index = (self.current_page - 1) * self.songs_per_page + (index - 1) # the raw index and current page are 1-based

        # get the song at the specified index
        song = self[index]

        # remove the song from the queue
        del self[index]

        # put the song at the top of the queue
        self.put_at_front(song)

    def reset_state(self):
        """
        Resets the queue state.
        """
        self.current_page = 1
        self.repeated_times = 0
        self.reset()