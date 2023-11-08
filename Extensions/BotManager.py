import logging
import os
import sys
import discord
from discord.ext import commands
from Replies.Strings import Messages
import Suica

# logging
log = logging.getLogger(__name__)

"""
Bot manager.
"""


class BotManager(commands.Cog):
    def __init__(self, bot: Suica.Bot):
        self.bot = bot
        self.bot.remove_command("help")

    # Event listeners
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Suica has been booted!")
        """
        await self.bot.get_channel(int(self.bot.backstage_channel)).send(
            Messages.BOT_BOOTED
        )
        """
        await self.bot.change_presence(
            activity=discord.CustomActivity(self.bot.status_message),
            status=discord.Status.online
        )

    @commands.Cog.listener()
    async def on_resumed(self):
        log.info("Suica has been resumed?")

    # Command event listeners
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound) or isinstance(
            error, commands.CheckFailure
        ):
            if ctx.message.content.count(f"{self.bot.prefix}") > 1:
                return
            await ctx.message.add_reaction("❓")
        else:
            await ctx.message.add_reaction("❌")
            raise error
        
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        await ctx.message.add_reaction("✅")

    # Commands
    @commands.is_owner()
    @commands.command(name="reload", disabled=True)
    async def _reload(self, ctx):
        """
        Hot reloads all extensions.
        Currently disabled because it doesn't play well with the jukebox.
        """
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

    # restart the bot
    @commands.is_owner()
    @commands.command(name="restart")
    async def _restart(self, ctx):
        """
        Restarts the bot.
        """
        await ctx.send(Messages.BOT_RESTARTING)
        # await self.bot.close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # shutdown the bot (temporarily here cuz the restart command does not play well with discord's login system)
    @commands.is_owner()
    @commands.command(name="shutdown")
    async def _shutdown(self, ctx):
        """
        Shuts down the bot and logs it out.
        """
        await ctx.send("Shutting down...")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(BotManager(bot))
    log.info("Module loaded")
