import logging
import discord
from discord.ext import commands
from Extensions.JukeboxHelpers.Errors import *
from Extensions.JukeboxHelpers.Player import Player
from Replies.Messages import Messages
from Replies.Embeds import JukeboxEmbeds
from Replies.Embeds import Helpers # TODO: Consider refactoring this to a separate module

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
        """
        Returns the player associated with the guild relevant command was invoked from.
        """
        player = self.node.get_player(ctx.guild.id)
        if not player:
            # make a new player
            player = Player()
            player.bounded_channel = ctx.channel
        return player

    # Get the next song in queue when the current song ends
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        """
        This event is triggered when the current song ends. It automatically plays the next song in queue.
        """
        try:
            if not payload.player.autoplay:
                await payload.player.advance()
            else:
                pass # to be implemented
        except QueueIsEmpty:
            pass
            # await payload.player.bounded_channel.send(Messages.JUKEBOX_NO_MORE_SONGS.format(self.bot.prefix))

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

        player: Player = await self.get_player(ctx)

        vc: Player = await channel.connect(cls=player)
        await ctx.send(Messages.JUKEBOX_JOIN.format(channel.name))

        await player.set_volume(100)

        return player

    @_join.error
    async def _join_error(self, ctx: commands.Context, error):
        error = error.original
        if isinstance(error, discord.ClientException):
            if error.args[0] == "Already connected to a voice channel.":
                return await ctx.send(Messages.JUKEBOX_ALREADY_CONNECTED)
        else:
            raise error

    @commands.command(name="leave", aliases=["disconnect", "l", "d", "dc"])
    async def _leave(self, ctx: commands.Context):
        """
        Disconnects from a voice channel
        """
        player: Player = await self.get_player(ctx)
        await player.teardown()

        await ctx.message.add_reaction("👋")
        await ctx.message.add_reaction("✅")

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, *, query: str):
        """
        Plays a song. Accepts a YouTube URL or a search query as an argument.
        """
        # join the voice channel if not already
        if not any(vc.guild == ctx.guild for vc in self.bot.voice_clients):
            await ctx.invoke(self._join)

        player: Player = await self.get_player(ctx)

        # pre-process the query
        processed_query = query.strip("<>")

        # extra message when adding a song from YT's playlist view
        if "&list=" in query:
            processed_query = processed_query.split("&list=")[0]
            correct_url = (
                "<https://www.youtube.com/playlist?list="
                + query.split("&list=")[1]
                + ">"
            )
            await ctx.send(
                Messages.JUKEBOX_PLAYLIST_INFO.format(self.bot.prefix, correct_url)
            )

        # perform the query
        await ctx.send(Messages.JUKEBOX_SEARCHING.format(processed_query))
        await ctx.typing()  # typing indicator for UX
        tracks = await wavelink.YouTubeTrack.search(processed_query)
        if not tracks:
            await ctx.send(Messages.JUKEBOX_NO_MATCHES.format(processed_query))
            if "/playlist?" in query:
                await ctx.send(Messages.JUKEBOX_PLAYLIST_PRIVATE)
            return

        # add the song(s) to queue
        new_track = await player.add(ctx, tracks)

        # extra message when importing a playlist
        if "/playlist?" in query:
            await ctx.send(
                Messages.JUKEBOX_IMPORTED_PLAYLIST.format(len(tracks.tracks))
            )

        # display the song info
        embed = JukeboxEmbeds.NewSongEmbed(ctx=ctx, track=new_track)
        await ctx.send(embed=embed)

        # extra message when the song playing is a stream
        if player.current.is_stream:
            await ctx.send(Messages.JUKEBOX_STREAM_WARNING.format(self.bot.prefix))

    @commands.command(name="pause", aliases=["pa", "stop"])
    async def _pause(self, ctx: commands.Context):
        """
        Pauses the player if playing
        """
        player: Player = await self.get_player(ctx)

        await player.pause()

        await ctx.message.add_reaction("⏸️")
        await ctx.message.add_reaction("✅")

    @commands.command(name="resume", aliases=["re"])
    async def _resume(self, ctx):
        """
        Resumes the player if paused
        """
        player: Player = await self.get_player(ctx)

        await player.resume()

        await ctx.message.add_reaction("▶️")
        await ctx.message.add_reaction("✅")

    @commands.command(
        name="skip", aliases=["sk"]
    )  # which is essentially a stop, but the player will play the next song in queue
    async def _skip(self, ctx: commands.Context):
        """
        Skips the current playing song
        """
        player: Player = await self.get_player(ctx)

        if player.is_looping_one:
            await player.toggle_loop_one(ctx)
            await ctx.send(Messages.JUKEBOX_LOOP_ONE_DISABLED_AUTO)

        await player.stop()
        await ctx.message.add_reaction("⏭️")
        await ctx.message.add_reaction("✅")

    @commands.command(name="back", aliases=["pr", "prev"])
    async def _back(self, ctx: commands.Context):
        """
        Goes back to the previous song
        """
        player: Player = await self.get_player(ctx)

        player.go_back()
        if player.is_playing():
            await player.stop() # have to do it here for the event listener to pick up
        else:
            await player.advance()

        if player.is_looping_one:
            await player.toggle_loop_one(ctx)
            await ctx.send(Messages.JUKEBOX_LOOP_ONE_DISABLED_AUTO)
        
        await ctx.message.add_reaction("⏮️")
        await ctx.message.add_reaction("✅")

    @commands.command(name="queue", aliases=["q", "qu"])
    async def _queue(self, ctx: commands.Context, page: int | str = 1):
        """
        Displays the current queue. Accepts a page number as an argument. Page number defaults to 1.
        Also accepts ">" and "<" as arguments to navigate to the next and previous page respectively.
        """
        player: Player = await self.get_player(ctx)

        await ctx.send(
            embed=JukeboxEmbeds.QueueEmbed(guild=ctx.guild, player=player, page=page)
        )

    @commands.command(name="nowplaying", aliases=["np", "now", "playing", "nowplay"])
    async def _nowplaying(self, ctx: commands.Context):
        """
        Displays the currently playing song, its progress and player volume
        """
        player: Player = await self.get_player(ctx)

        await ctx.send(embed=JukeboxEmbeds.NowPlayEmbed(guild=ctx.guild, player=player))

    @commands.command(name="volume", aliases=["vol"])
    async def _volume(self, ctx, *, volume: int):
        """
        Sets the player volume. Accepts a number between 0 and 100.
        """
        player: Player = await self.get_player(ctx)

        current_volume = player.volume

        # cap volume between 0 and 100
        volume = max(min(volume, 100), 0)
        await player.set_volume(volume)

        await ctx.message.add_reaction("🔊")
        if current_volume < volume:
            await ctx.message.add_reaction("⬆")
        else:
            await ctx.message.add_reaction("⬇")
        await ctx.message.add_reaction("✅")

    @commands.command(name="shuffle", aliases=["sh", "shuf"])
    async def _shuffle(self, ctx):
        """
        Shuffles the queue
        """
        player: Player = await self.get_player(ctx)

        player.shuffle()

        await ctx.message.add_reaction("🔀")
        await ctx.message.add_reaction("✅")

    @commands.command(name="repeat", aliases=["loop", "lp"])
    async def _repeat(self, ctx):
        """
        Toggles repeat one mode
        """
        player: Player = await self.get_player(ctx)

        await player.toggle_loop_one(ctx)

        if player.is_looping_one:
            await ctx.message.add_reaction("🔂")
        else:
            await ctx.message.add_reaction("➡")
        await ctx.message.add_reaction("✅")

    @commands.command(name="repeatall", aliases=["loopall", "lpa"])
    async def _repeatall(self, ctx):
        """
        Toggles repeat all mode
        """
        player: Player = await self.get_player(ctx)

        await player.toggle_loop_all(ctx)

        if player.is_looping_all:
            await ctx.message.add_reaction("🔁")
        else:
            await ctx.message.add_reaction("➡")
        await ctx.message.add_reaction("✅")

    @commands.command(name="top", aliases=["tp"])
    async def _top(self, ctx, index: int, skip: str = None):
        """
        Moves the song at the specified index to the top of the queue.
        Accepts a number from 1 to 10 as an argument.
        If another argument "-s" is provided, the current song will be skipped.
        """
        player: Player = await self.get_player(ctx)

        try:
            player.move_song_to_top(index)
        except IndexError:
            pass

        if skip == "-s":
            await ctx.invoke(self._skip)

        await ctx.message.add_reaction("⏫")
        await ctx.message.add_reaction("✅")

    @commands.command(name="remove", aliases=["rm"])
    async def _remove(self, ctx, index: int):
        """
        Removes the song at the specified index from the queue.
        Accepts a number from 1 to 10 as an argument.
        """
        player: Player = await self.get_player(ctx)

        try:
            song_removed: wavelink.Playable = player.remove_song(index)
        except:
            pass

        await ctx.send(Messages.JUKEBOX_SONG_REMOVED.format(song_removed.title))


    @commands.command(name="clear", aliases=["clr", "cl"])
    async def _clear(self, ctx, history: str = None):
        """
        Clears the queue and keeps the current song playing
        If another argument "-h" is provided, the history queue will be also cleared.
        """
        player: Player = await self.get_player(ctx)

        player.clear()

        if history == "-h":
            player.clear_history()

        await ctx.message.add_reaction("🗑️")
        await ctx.message.add_reaction("✅")

    @commands.command(name="seek", aliases=["se"])
    async def _seek(self, ctx, time: str):
        pass

    # TODO: Implement proper autoplay
    @commands.command(name="autoplay", aliases=["ap"], enabled=False)
    async def _autoplay(self, ctx):
        player: Player = await self.get_player(ctx)

        player.toggle_auto_play()

        if player.autoplay:
            await ctx.send(Messages.JUKEBOX_AUTOPLAY_ENABLED)
        else:
            await ctx.send(Messages.JUKEBOX_AUTOPLAY_DISABLED)


async def setup(bot):
    await bot.add_cog(Jukebox(bot))
    log.info("Module loaded")
