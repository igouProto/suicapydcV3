import logging
from discord.ext import commands
from Replies.Strings import Messages

# logging
log = logging.getLogger(__name__)

"""
Template for new extensions.
"""


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Template(bot))
    log.info("Module loaded")
