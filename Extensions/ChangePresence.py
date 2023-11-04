import logging
import discord
from discord.ext import commands
from Replies.Messages import Messages

# logging
log = logging.getLogger(__name__)

"""
Command for changing the bot's presence.
"""


class ChangePresence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    TODO: 
    - Emoji support
    - Revert to default after a certain amount of time
    """

    @commands.is_owner()
    @commands.command(name="presence", aliases=["cp"])
    async def _change_presence(self, ctx, *, message):
        self.bot.status_message = message

        # Revert to default
        if message == "default":
            self.bot.status_message = Messages.DEFAULT_STATUS_MESSAGE.format(self.bot.version, self.bot.prefix)

        await self.bot.change_presence(
            activity=discord.CustomActivity(self.bot.status_message)
        )
        await ctx.send(Messages.PRESENCE_CHANGED.format(self.bot.status_message))


async def setup(bot):
    await bot.add_cog(ChangePresence(bot))
    log.info("Module loaded")
