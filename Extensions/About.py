import logging
import discord
from discord.ext import commands
from Replies.Strings import Messages
import Suica

# logging
log = logging.getLogger(__name__)

"""
About Suica!
"""


class About(commands.Cog):
    def __init__(self, bot: Suica.Bot):
        self.bot = bot

    @commands.command(name="about")
    async def about(self, ctx):
        
        # retrieve bot info
        bot_info = await self.bot.application_info()
        bot_id = bot_info.id
        name = bot_info.name
        owner = bot_info.owner.mention
        borntime = "2018-08-01 05:47:51.880000"

        embed = discord.Embed(title='**S**ugoi **U**ltra **I**ntelligent **C**hat **A**ssistant, SUICA', colour=discord.Color.orange())
        embed.set_author(name=Messages.ABOUT_TITLE, icon_url=self.bot.user.avatar.url)
        embed.description = Messages.ABOUT.format(bot_id, name, owner, borntime)
        embed.set_footer(text=Messages.ABOUT_FOOTER.format(self.bot.version))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
    log.info("Module loaded")
