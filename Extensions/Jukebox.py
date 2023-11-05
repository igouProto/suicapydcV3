from ast import alias
import asyncio
from calendar import c
import logging
import discord
from discord.ext import commands
from Extensions.JukeboxHelpers.Errors import *
from Extensions.JukeboxHelpers.Player import Player
from Replies.Messages import Messages

import wavelink

# logging
log = logging.getLogger(__name__)

"""
The main command interface for the jukebox
"""


class Jukebox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.node = None

    # Create and connect to a lavalink node
    @commands.Cog.listener()
    async def on_ready(self):
        await self.start_nodes()
        node = wavelink.NodePool.get_node()
        self.node = node

    async def start_nodes(self):
        node: wavelink.Node = wavelink.Node(
            uri="http://127.0.0.1:2333", password="igproto"
        )
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])

    # Event listeners
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        log.info(f"Connected to lavalink node {node.id}")

    # Helper functions
    # Get player from guild, create one if not found
    async def get_player(self, ctx):
        self.print_status()
        player = self.node.get_player(ctx.guild.id)
        if not player:
            # make a new player
            player = Player()
            player.bounded_channel = ctx.channel
        return player

    # Get the next song in queue when the current song ends
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        print("track ended")
        await payload.player.advance()

    def print_status(self):
        print("--------------------")
        print(self.node.players)

    # Commands
    @commands.command(name="join", aliases=["connect", "j", "c", "summon"])
    async def _join(
        self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None
    ):
        """
        Connects to a voice channel
        """
        try:
            channel = channel or ctx.author.voice.channel
        except AttributeError:
            await ctx.send(Messages.JUKEBOX_NO_VOICE_CHANNEL)
            raise NoVoiceChannel

        player = await self.get_player(ctx)

        vc: Player = await channel.connect(cls=player)
        await ctx.send(Messages.JUKEBOX_JOIN.format(channel.name))

        self.print_status()
        return player

    @_join.error
    async def _join_error(self, ctx, error):
        error = error.original
        if isinstance(error, discord.ClientException):
            if error.args[0] == "Already connected to a voice channel.":
                return await ctx.send(Messages.JUKEBOX_ALREADY_CONNECTED)
        else:
            raise error

    @commands.command(name="leave", aliases=["disconnect", "l", "d", "dc"])
    async def _leave(self, ctx):
        """
        Disconnects from a voice channel
        """
        player = await self.get_player(ctx)
        await player.teardown()
        await ctx.send(Messages.JUKEBOX_LEAVE)

        # self.print_status()

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx, *, query: str):
        # join the voice channel if not already
        if not any(vc.guild == ctx.guild for vc in self.bot.voice_clients):
            await ctx.invoke(self._join)

        player = await self.get_player(ctx)
        
        await ctx.typing()

        # pre-process the query
        processed_query = query.strip("<>")
        # treat non-url queries as youtube searches
        if not query.startswith("http"):
            processed_query = f"ytsearch:{query}"

        await ctx.send(Messages.JUKEBOX_SEARCHING.format(processed_query))
        tracks = await wavelink.GenericTrack.search(processed_query)
        if not tracks:
            return await ctx.send(Messages.JUKEBOX_NO_MATCHES.format(processed_query))
        
        # add the song to queue
        new_track = await player.add(ctx, tracks)

        # display the song info
        await ctx.send(f":musical_note: **{new_track.title}**")

    @commands.command(name="pause")
    async def _pause(self, ctx):
        pass

    @commands.command(name="resume")
    async def _resume(self, ctx):
        pass

    @commands.command(name="stop")
    async def _stop(self, ctx):
        pass

    @commands.command(name="skip") # which is essentially a stop, but the player will play the next song in queue
    async def _skip(self, ctx):
        pass

    @commands.command(name="queue", aliases=["q"])
    async def _queue(self, ctx):
        pass

    @commands.command(name="nowplaying", aliases=["np", "now", "playing"])
    async def _nowplaying(self, ctx):
        pass

    @commands.command(name="volume", aliases=["vol"])
    async def _volume(self, ctx, *, volume: int):
        pass

    @commands.command(name="shuffle", aliases=["sh", "shuf"])
    async def _shuffle(self, ctx):
        pass

    @commands.command(name="repeat", aliases=["loop", "lp"])
    async def _repeat(self, ctx):
        pass

    @commands.command(name="repeatall", aliases=["loopall", "lpa"])
    async def _repeatall(self, ctx):
        pass

    # new! autoplay toggle
    @commands.command(name="autoplay", aliases=["ap"])
    async def _autoplay(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(Jukebox(bot))
    log.info("Module loaded")
