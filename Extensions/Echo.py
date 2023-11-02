from calendar import c
import logging
from discord.ext import commands
from Replies.Messages import Messages

# logging
log = logging.getLogger(__name__)

"""
This extension lets you talk through the bot.
"""


class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, destination, message):
        await self.bot.get_channel(int(destination)).send(message)


async def setup(bot):
    await bot.add_cog(Echo(bot))
    log.info("Module loaded")
