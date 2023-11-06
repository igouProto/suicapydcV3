import logging
from discord.ext import commands
from Replies.Strings import Messages

# logging
log = logging.getLogger(__name__)

"""
Displays the user manual.
"""


class Manual(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="manual", aliases=["man", "help"])
    async def manual(self, ctx: commands.Context):
        """
        Display manual from file.
        """
        with open("Assets/manual.txt", "r", encoding="utf-8") as f:
            await ctx.send(f.read())


async def setup(bot):
    await bot.add_cog(Manual(bot))
    log.info("Module loaded")
