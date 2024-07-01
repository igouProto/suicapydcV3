import asyncio
import logging
import discord
from discord.ext import commands
from Replies.Strings import Messages

# logging
log = logging.getLogger(__name__)

"""
Scans for twitter links, and if there's no embed, reply with a vxtwitter link.
"""


class AutoTwiEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if not (
            message.content.startswith("https://x.com")
            or message.content.startswith("https://twitter.com")
        ):
            return

        suffix = message.content.split(".com/")[1]

        # if we don't see images from the embed, reply with a vxtwitter link
        await asyncio.sleep(0.5)  # allow some time for embeds to come in

        # reply when: there's no embed / no image or image url is present
        if (
            not message.embeds
            or len(message.embeds) == 0
            or not message.embeds[0].image.url
        ):
            link = "https://fxtwitter.com/" + suffix
            await message.reply(link, mention_author=False)


async def setup(bot):
    await bot.add_cog(AutoTwiEmbed(bot))
    log.info("Module loaded")
