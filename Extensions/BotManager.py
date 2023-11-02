import logging
from discord.ext import commands
from Replies.Messages import Messages

# logging
log = logging.getLogger(__name__)

"""
Bot manager.
"""


class BotManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Suica has been booted!")

    # hot reloading all extensions
    @commands.is_owner()
    @commands.command(name="reload")
    async def _reload(self, ctx):
        await ctx.send(Messages.EXTENSION_RELOADING)
        # Get the list of extensions
        extentions = self.bot.extensions.copy()
        for extension in extentions:
            # Reload the extension
            try:
                await self.bot.reload_extension(extension)
            except Exception as e:
                log.error("Failed to reload extension {}: {}".format(extension, e))
        await ctx.send(Messages.EXTENSION_RELOADED)


async def setup(bot):
    await bot.add_cog(BotManager(bot))
    log.info("BotManager loaded")
