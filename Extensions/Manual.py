import logging
from discord.ext import commands
from Replies.Strings import Messages
import Suica

# logging
log = logging.getLogger(__name__)

"""
Displays the user manual.
"""


class Manual(commands.Cog):
    def __init__(self, bot: Suica.Bot):
        self.bot = bot

    @commands.command(name="manual", aliases=["man", "help"])
    async def manual(self, ctx: commands.Context):
        """
        Display manual from file.
        """
        with open("Assets/manual.txt", "r", encoding="utf-8") as f:
            manual = f.read() + f"\n`v{self.bot.version}`"
            await ctx.send(manual)


async def setup(bot):
    await bot.add_cog(Manual(bot))
    log.info("Module loaded")
