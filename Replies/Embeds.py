import discord
from .EmbedStrings import Constants

"""
Collection of embeds for the bot
"""


class PingEmbed(discord.Embed):
    def __init__(self, bot_latency, command_latency, voice_latency):
        super().__init__(
            title=Constants.PING_TITLE,
            color=discord.Color.green(),
            description=f"{Constants.PING_HEARTBEAT}: **{bot_latency}**ms\n{Constants.PING_REACTIONTIME}: **{command_latency}**ms\n{Constants.PING_VOICECLIENT}: **{voice_latency}**ms",
        )
