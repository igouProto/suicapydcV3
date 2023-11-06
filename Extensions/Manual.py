import logging
from discord.ext import commands
from Replies.Messages import Messages

# logging
log = logging.getLogger(__name__)

"""
Template for new extensions.
"""


class Manual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="manual", aliases=["man", "help"])
    async def manual(self, ctx: commands.Context):
        """
        Display manual from file.
        """


async def setup(bot):
    await bot.add_cog(Manual(bot))
    log.info("Module loaded")
