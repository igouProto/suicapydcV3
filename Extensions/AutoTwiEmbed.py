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
        
        if not message.content.startswith('https://x.com'):
            return
        
        await asyncio.sleep(0.5) # allow some time for embeds to come in

        # if we don't see images from the embed
        # replace original link with vxtwitter link
        if not message.embeds[0].image.url:
            link = message.embeds[0].url.replace("https://twitter.com/", "https://vxtwitter.com/")
            await message.reply(link, mention_author=False)
        


async def setup(bot):
    await bot.add_cog(AutoTwiEmbed(bot))
    log.info("Module loaded")
