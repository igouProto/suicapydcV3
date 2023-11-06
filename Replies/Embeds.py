import discord
from .EmbedStrings import Constants
from .Messages import Messages
from Extensions.JukeboxHelpers.Player import Player

import wavelink

from discord.ext import commands

"""
Collection of embeds for the bot
"""


class PingEmbed(discord.Embed):
    def __init__(self, bot_latency, command_latency, voice_latency):
        super().__init__(
            title=Constants.PING_TITLE,
            color=discord.Color.green(),
            description=(
                f"{Constants.PING_HEARTBEAT}: **{bot_latency}**ms\n"
                f"{Constants.PING_REACTIONTIME}: **{command_latency}**ms\n"
                f"{Constants.PING_VOICECLIENT}: **{voice_latency}**ms"
            ),
        )


class JukeboxEmbeds:
    color = discord.Color.red()

    class NowPlayEmbed(discord.Embed):
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
            self.set_author(name=Constants.JUKEBOX_NOWPLAY_TITLE, icon_url=guild.icon)
            self.set_thumbnail(url=thumbnail)

            if player and player.is_looping_one:
                self.set_footer(
                    text=Constants.JUKEBOX_LOOP_COUNT.format(player.loop_count)
                )

    class NewSongEmbed(discord.Embed):
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
                name=f"{Constants.JUKEBOX_NEW_SONG_ADDED.format(ctx.author.display_name)}",
                icon_url=ctx.author.display_avatar.url,
            )
            self.set_thumbnail(url=track.thumbnail)

    class QueueEmbed(NowPlayEmbed):
        def __init__(self, guild: discord.Guild, player: Player, page: int=1):
            super().__init__(guild, player)

            raw_page, page_num, max_page = player.get_paginated_queue(page=page)
            
            # compose a list of songs in the queue
            processed_page = Helpers().process_raw_page(raw_page)

            # if the list is empty, display a message instead
            if processed_page == "":
                processed_page = Constants.JUKEBOX_NOTHING_IN_QUEUE

            self.add_field(name=f"{Constants.JUKEBOX_QUEUE_UPNEXT}", value=processed_page, inline=False)

            footer = Constants.JUKEBOX_PAGINATION.format(page_num, max_page)
            if player.autoplay:
                footer += f"  •  {Constants.JUKEBOX_AUTOPLAY_ENABLED}"
            self.set_footer(text=footer)


class OmikijiEmbeds:
    pass


# Some helper functions for building the embeds
class Helpers:
    fallback_url = "https://127.0.0.1"

    def time_format(self, time):
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
        if "*" in raw_title:
            ind = raw_title.index("*")
            return_title = raw_title[:ind] + "\\" + raw_title[ind:]
            return return_title
        else:
            return raw_title

    def playback_status(self, player: Player):
        if player:
            track: wavelink.Playable | wavelink.YouTubeTrack = player.current
        else:
            track = None

        # if nothing is playing
        if not track:
            return self.fallback_url, f"{Constants.JUKEBOX_NOTHING_PLAYING}", "-- / --", "--", self.fallback_url

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
        processed_page = ""
        index = 1
        for item in raw_page:
            processed_page += f"`{index:02d}.` {item.title} `({Helpers().time_format(item.duration / 1000)})`\n"
            index += 1
        return processed_page
