import logging
import discord
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

    # Event listeners
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Suica has been booted!")
        await self.bot.get_channel(int(self.bot.backstage_channel)).send(
            Messages.BOT_BOOTED
        )
        await self.bot.change_presence(
            activity=discord.CustomActivity(self.bot.status_message)
        )

    @commands.Cog.listener()
    async def on_resumed(self):
        log.info("Suica has been resumed?")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound) or isinstance(
            error, commands.CheckFailure
        ):
            if ctx.message.content.count(f"{self.bot.prefix}") > 1:
                return
            await ctx.message.add_reaction("❓")

    # hot reloading all extensions
    @commands.is_owner()
    @commands.command(name="reload")
    async def _reload(self, ctx):
        await ctx.send(Messages.EXTENSION_RELOADING)
        # Get the list of extensions
        extentions = self.bot.extensions.copy()
        # Reload the extensions and track if any failed
        failed = []
        success_count = 0
        for extension in extentions:
            try:
                await self.bot.reload_extension(extension)
                success_count += 1
            except Exception as e:
                log.error("Failed to reload extension {}: {}".format(extension, e))
                failed.append(f"{extension}: {e}")
        # Report the results
        await ctx.send(
            Messages.EXTENSION_RELOADED.format(success_count, len(extentions))
        )
        if len(failed) > 0:
            failed_list = "\n".join(failed)
            await ctx.send(
                Messages.EXTENSION_RELOAD_FAILED.format(f"```{failed_list}```")
            )


async def setup(bot):
    await bot.add_cog(BotManager(bot))
    log.info("Module loaded")
