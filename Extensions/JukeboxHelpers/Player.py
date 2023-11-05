from hmac import new
from operator import is_
from typing import Any
import wavelink
import discord
from .Queue import Queue
from .Errors import *

class Player(wavelink.Player):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        
        self.queue = Queue()
        self.bounded_channel = None
    
    async def teardown(self):
        try:
            await super().disconnect()
        except KeyError:
            pass

    # Queue management
    async def add(self, ctx, tracks):        
        if (isinstance(tracks, wavelink.YouTubePlaylist)):
                self.queue.put(*tracks.tracks)
        else:
            self.queue.put(tracks[0])
        
        new_track = self.queue[0]

        # play the song if the queue is empty or if the player is not playing
        if self.queue.is_empty or not self.is_playing():
            print("auto play track added to queue")
            await self.play(self.queue.get())

        return new_track

    # move to the next song. should be triggered when the current song ends
    async def advance(self):
        if self.queue.is_empty:
            raise QueueIsEmpty
        
        await self.play(self.queue.get())

        # print("advanced to next song")
        # print(self.queue)
        # print(self.queue.history)

        # counting repeated times cuz i'm bored
        if (self.queue.loop):
            self.queue.repeated_times += 1
        else:
            self.queue.repeated_times = 0
        