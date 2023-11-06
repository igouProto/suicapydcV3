from calendar import c
import logging
from discord.ext import commands
from Replies.Strings import Messages

# logging
log = logging.getLogger(__name__)

"""
This extension lets Suica echo messages.
"""


class Echo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, destination, message=None):
        """
        Echoes the message to the specified channel.
        """
        if message:
            await self.bot.get_channel(int(destination)).send(message)
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                await self.bot.get_channel(int(destination)).send(attachment.url)

    @commands.command(name="pekofy", aliases=["peko"])
    async def pekofy(self, ctx, message=None):
        """
        Pekofy a message. Adds "peko" to the end of the message and echoes it.
        """
        if message:
            await ctx.send(message + " peko")

        if message == "pain":  # pain-peko
            await ctx.send(
                "https://i.pinimg.com/736x/f3/ff/0b/f3ff0bfe160d84d6f85bb53c06319406.jpg"
            )


async def setup(bot):
    await bot.add_cog(Echo(bot))
    log.info("Module loaded")
