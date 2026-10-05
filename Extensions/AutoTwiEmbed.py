import asyncio
import logging
import re
import aiohttp
import discord
from discord.ext import commands
from Replies.Strings import Messages

# logging
log = logging.getLogger(__name__)

"""
Scans for twitter links, and replies with a vxtwitter link when twitter's own embed
isn't good enough:
- no embed at all
- an "age-restricted content" placeholder embed
- a media preview (video / gif / multi-image posts). vxtwitter's API is asked what
  the media is, and we reply only if there's a video / gif (or if we can't tell)
- an embed with neither description nor a twitter-hosted image
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

        await asyncio.sleep(
            self.timeout / 1000
        )  # allow some (configurable, but not permanent atm) time for embeds to come in

        link = "https://vxtwitter.com/" + suffix

        # Got no embed -> append one

        if not message.embeds or len(message.embeds) == 0:
            await message.reply(link, mention_author=False)
            return

        # Other cases when there is an embed but not what we wanted

        embed = message.embeds[0]
        desc = embed.description

        # Case: Twitter serving an "Age-restricted content" preview
        if self._is_age_restricted(embed):
            await self._reply_and_clean(message, link)
            return

        # Case: Twitter serving a media preview for video / gif / multi-image posts
        # reply only when non-image media exists. twitter handles multi-image posts well
        # we ask the all-mighty vxtwitter to find out which
        # but if we still don't know we reply anyway
        if self._has_media_preview(embed):
            match = re.search(r"/status/(\d+)", suffix)
            data = await self._fetch_tweet_info(match.group(1)) if match else None

            if data is None or self._has_non_image_media(data):
                await self._reply_and_clean(message, link)
            return

        # Case: An embed without desc AND image
        if not desc and (
            not embed.image.url
            or not embed.image.url.startswith("https://pbs.twimg.com/")
        ):
            await self._reply_and_clean(message, link)

    # Configurable timeout as sometimes the embeds take a bit longer to come in
    @commands.command(name="settwitimeout", aliases=["twito"])
    @commands.is_owner()
    async def _set_twit_timeout(self, ctx, timeout: int = None):

        if not timeout:
            await ctx.send(Messages.TWI_TIMEOUT_CURRENT.format(self.timeout))
            return

        self.timeout = timeout
        await ctx.send(Messages.TWI_TIMEOUT_SET.format(timeout))

    @staticmethod
    async def _reply_and_clean(message: discord.Message, link: str) -> None:
        await message.reply(link, mention_author=False)
        try:
            await message.edit(suppress=True)
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            log.warning("couldn't suppress embeds on message %s", message.id)

    @staticmethod
    def _is_age_restricted(embed: discord.Embed) -> bool:
        # the notice lives in the description, with markdown escapes ("Age\\-restricted")
        desc = (embed.description or "").replace("\\", "").lower()
        return "age-restricted" in desc

    @staticmethod
    def _has_media_preview(embed: discord.Embed) -> bool:
        # for videos / gifs / multi-image posts, twitter's own embed only shows a generated
        # preview (".../media-preview/<id>") instead of a pbs.twimg.com photo
        return "media-preview" in (embed.image.url or "")

    @staticmethod
    def _has_non_image_media(data: dict) -> bool:
        # only look at the outer tweet's media, a quoted tweet has its own (nested "qrt")
        return any(m.get("type") != "image" for m in data.get("media_extended", []))

    @staticmethod
    async def _fetch_tweet_info(post_id: str) -> dict | None:
        url = f"https://api.vxtwitter.com/Twitter/status/{post_id}"
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5)
            ) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        log.warning(
                            "vxtwitter api returned %s for %s", resp.status, post_id
                        )
                        return None
                    return await resp.json()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            log.exception("vxtwitter api call failed for %s", post_id)
            return None


async def setup(bot):
    await bot.add_cog(AutoTwiEmbed(bot))
    log.info("Module loaded")
