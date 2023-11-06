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
    async def echo(self, ctx, destination, message=None):
        if message:
            await self.bot.get_channel(int(destination)).send(message)
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await self.bot.get_channel(int(destination)).send(attachment.url)

    # add "peko" to the end of the message cuz why not
    @commands.command(name="pekofy", aliases=["peko"])
    async def pekofy(self, ctx, message=None):
        if message:
            await ctx.send(message + " peko")

        if message == "pain": # pain-peko
            await ctx.send("https://i.pinimg.com/736x/f3/ff/0b/f3ff0bfe160d84d6f85bb53c06319406.jpg")


async def setup(bot):
    await bot.add_cog(Echo(bot))
    log.info("Module loaded")
