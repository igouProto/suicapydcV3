from time import localtime, strftime
import discord

from Extensions.OmikujiHelpers.Omikuji import FortuneResult
from .Strings import Messages, EmbedStrings
from Extensions.JukeboxHelpers.Player import Player

import wavelink

from discord.ext import commands

"""
Collection of embeds of Suica.
PingEmbed is the embed for the ping command.
JukeboxEmbeds contains embeds associated with the jukebox, including a nowplay display, a queue display, and a new song display.
OmikujiEmbeds contains embeds for the omikuji command.
Helpers is a collection of helper functions that might be useful when building embeds.
"""


class PingEmbed(discord.Embed):
    """
    Embed for the ping command. Takes in the bot latency, command latency, and voice latency as parameters.
    """

    def __init__(self, bot_latency: int, command_latency: int, voice_latency: int):
        super().__init__(
            title=EmbedStrings.PING_TITLE,
            color=discord.Color.green(),
            description=(
                f"{EmbedStrings.PING_HEARTBEAT}: **{bot_latency}**ms\n"
                f"{EmbedStrings.PING_REACTIONTIME}: **{command_latency}**ms\n"
                f"{EmbedStrings.PING_VOICECLIENT}: **{voice_latency}**ms"
            ),
        )


class JukeboxEmbeds:
    """
    Collection of embeds associated with the jukebox.
    """

    color = discord.Color.red()

    class NowPlayEmbed(discord.Embed):
        """
        Embed for displaying the song currently playing in the guild.
        """

        def __init__(self, guild: discord.Guild, player: Player):
            super().__init__(
                color=JukeboxEmbeds.color,
            )

            (
                uri,
                title,
                progress_display,
                volume_display,
                thumbnail,
            ) = Helpers().playback_status(player)

            self.title = f"{title}"
            self.url = uri
            self.description = f"{progress_display}  •  {volume_display}"
            self.set_author(
                name=EmbedStrings.JUKEBOX_NOWPLAY_TITLE, icon_url=guild.icon
            )
            self.set_thumbnail(url=thumbnail)

            if player and player.is_looping_one:
                self.set_footer(
                    text=EmbedStrings.JUKEBOX_LOOP_COUNT.format(player.loop_count)
                )

    class NewSongEmbed(discord.Embed):
        """
        Embed for displaying a new song added to the queue.
        """

        def __init__(self, ctx: commands.context, track: wavelink.YouTubeTrack):
            super().__init__(
                color=JukeboxEmbeds.color,
            )

            self.title = f"**{track.title}**"
            self.url = track.uri

            if track.is_stream:
                self.description = f"` 🔴 LIVE `  •  {track.author}"
            else:
                self.description = (
                    f"{Helpers().time_format(track.duration / 1000)}  •  {track.author}"
                )

            self.set_author(
                name=f"{EmbedStrings.JUKEBOX_NEW_SONG_ADDED.format(ctx.author.display_name)}",
                icon_url=ctx.author.display_avatar.url,
            )
            self.set_thumbnail(url=track.thumbnail)

    class QueueEmbed(NowPlayEmbed):
        """
        Embed for displaying the song currently playing in the guild + the queue.
        Supports pagination.
        """

        def __init__(self, guild: discord.Guild, player: Player, page: int = 1):
            super().__init__(guild, player)

            raw_page, page_num, max_page = player.get_paginated_queue(page=page)

            # compose a list of songs in the queue
            processed_page = Helpers().process_raw_page(raw_page)

            # if the list is empty, display a message instead
            if processed_page == "":
                processed_page = EmbedStrings.JUKEBOX_NOTHING_IN_QUEUE

            self.add_field(
                name=f"{EmbedStrings.JUKEBOX_QUEUE_UPNEXT}",
                value=processed_page,
                inline=False,
            )

            footer = EmbedStrings.JUKEBOX_PAGINATION.format(page_num, max_page)
            if player.autoplay:
                footer += f"  •  {EmbedStrings.JUKEBOX_AUTOPLAY_ENABLED}"
            self.set_footer(text=footer)


class OmikujiEmbeds:
    """
    Embeds for the omikuji command. Displays the omikuji result.
    """

    color = discord.Color.orange()

    class Omikuji(discord.Embed):
        def __init__(self, ctx: commands.Context, result: FortuneResult):
            super().__init__(
                color=OmikujiEmbeds.color,
                title=f"{result.fortune}",
                description=f"{result.determination}",
            )

            self.set_author(
                name=EmbedStrings.OMIKUJI_TITLE.format(ctx.author.display_name),
                icon_url=ctx.author.display_avatar.url,
            )

            self.add_field(
                name=EmbedStrings.OMIKUJI_DIRECTION, value=result.direction, inline=True
            )
            self.add_field(
                name=EmbedStrings.OMIKUJI_GACHAINDEX,
                value=f"☆ {result.gacha_index}",
                inline=True,
            )
            self.add_field(
                name=EmbedStrings.OMIKUJI_CHARGEINDEX,
                value=f"☆ {result.charge_index}",
                inline=True,
            )
            self.add_field(
                name=EmbedStrings.OMIKUJI_LUCKYNUMBER,
                value=result.lucky_number,
                inline=True,
            )
            self.add_field(
                name=EmbedStrings.OMIKUJI_LUCKYCOLOR,
                value=result.lucky_color,
                inline=True,
            )

            self.set_footer(
                text=EmbedStrings.OMIKUJI_FOOTER.format(
                    result.serial_number, strftime("%Y/%m/%d", localtime())
                )
            )


# Some helper functions for building the embeds
class Helpers:
    """
    Collection of helper functions that might be useful when building embeds.
    """

    fallback_url = "https://127.0.0.1"

    def time_format(self, time):
        """
        Format the time in seconds to xx:xx:xx format.
        """
        minutes, seconds = divmod(
            int(time), 60
        )  # minutes = duration / 60, second = duration % 60
        hours, minutes = divmod(
            int(minutes), 60
        )  # hours = minutes / 60, minutes = minutes % 60
        duration = []
        if hours > 0:
            duration.append(f"{hours}")
        duration.append(f"{minutes:02d}")
        duration.append(f"{seconds:02d}")

        return ":".join(duration)

    def title_parser(self, raw_title):
        """
        Escapes all the asterisks in the title to avoid Discord making the title italic.
        """
        if "*" in raw_title:
            ind = raw_title.index("*")
            return_title = raw_title[:ind] + "\\" + raw_title[ind:]
            return return_title
        else:
            return raw_title

    def playback_status(self, player: Player):
        """
        Displays the playback status of the player.
        Returns a tuple of uri, title, progress_display, volume_display, thumbnail.
        """
        if player:
            track: wavelink.Playable | wavelink.YouTubeTrack = player.current
        else:
            track = None

        # if nothing is playing
        if not track:
            return (
                self.fallback_url,
                f"{EmbedStrings.JUKEBOX_NOTHING_PLAYING}",
                "-- / --",
                "--",
                self.fallback_url,
            )

        title = self.title_parser(track.title)
        uri = track.uri
        duration = self.time_format(track.duration / 1000)
        position = self.time_format(player.position / 1000)
        volume = player.volume

        # the status display
        pause_icon = ""
        loop_icon = ""
        if player.is_paused():
            pause_icon = "⏸️"
        elif player.is_playing():
            pause_icon = "▶️"

        if player.queue.is_looping_one:
            loop_icon = "🔂"
        elif player.queue.is_looping_all:
            loop_icon = "🔁"

        status_display = f"{pause_icon} {loop_icon}"

        # progress in xx:xx/xx:xx format
        if track.is_stream:
            progress_display = f"` 🔴 LIVE `"
        else:
            progress_display = f"{status_display} {position} / {duration}"

        # volume in xx% format
        volume_display = f"🔊 {volume}%"

        # thumbnail
        thumbnail = track.thumbnail

        return uri, title, progress_display, volume_display, thumbnail

    def process_raw_page(self, raw_page):
        """
        Convert the raw page of songs into a list of songs that contains the index, song title, and duration.
        """
        processed_page = ""
        index = 1
        for item in raw_page:
            processed_page += f"`{index:02d}.` {item.title} `({Helpers().time_format(item.duration / 1000)})`\n"
            index += 1
        return processed_page
