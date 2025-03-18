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
        self.timeout = 500  # ms

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

        await asyncio.sleep(
            self.timeout / 1000
        )  # allow some (configurable, but not permanent atm) time for embeds to come in
        
        # reply when: there's no embed / no image or image url is present / embed with no img and desc
        # new condition: no image from twitter's photo blob storage is present

        # if there's no embed at all we also append one
        if not message.embeds or len(message.embeds) == 0:
            link = "https://fxtwitter.com/" + suffix
            await message.reply(link, mention_author=False)
            return

        embed = message.embeds[0]
        desc = embed.description

        # if there's an embed without desc AND image, we append one too
        if not desc and (
            not embed.image.url
            or not embed.image.url.startswith("https://pbs.twimg.com/")
        ):  # omg elon stop changing stuff...
            link = "https://fxtwitter.com/" + suffix
            await message.reply(link, mention_author=False)

    # configurable timeout
    # sometimes the embeds do take a longer while to come in
    @commands.command(name="settwitimeout", aliases=["twito"])
    @commands.is_owner()
    async def _set_twit_timeout(self, ctx, timeout: int = None):

        if not timeout:
            await ctx.send(Messages.TWI_TIMEOUT_CURRENT.format(self.timeout))
            return

        self.timeout = timeout
        await ctx.send(Messages.TWI_TIMEOUT_SET.format(timeout))


async def setup(bot):
    await bot.add_cog(AutoTwiEmbed(bot))
    log.info("Module loaded")
