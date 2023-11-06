import logging
from discord.ext import commands
from Replies.Messages import Messages
from Replies.Embeds import OmikujiEmbeds
from Extensions.OmikujiHelpers.Omikuji import FortuneResult, Generator
# logging
log = logging.getLogger(__name__)

"""
Omikuji module
"""


class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="omikuji", aliases=["omkj"])
    async def omikuji(self, ctx: commands.Context, force: str = None):

        if force == "-f":
            force = True
        results = Generator().generate(id=ctx.author.id, force=force)

        embed = OmikujiEmbeds.Omikuji(ctx, results)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Omikuji(bot))
    log.info("Module loaded")