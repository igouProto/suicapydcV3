from discord.ext import commands


class BotManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready.")


async def setup(bot):
    await bot.add_cog(BotManager(bot))
    print("BotManager loaded")