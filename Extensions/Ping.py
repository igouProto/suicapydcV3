import logging
from discord.ext import commands
from Replies.Messages import Messages
from Replies.Embeds import PingEmbed

# logging
log = logging.getLogger(__name__)

"""
Ping function.
"""


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def _ping(self, ctx):
        t = await ctx.send(Messages.PINGING)

        # Calculate latency
        bot_latency = round(self.bot.latency * 1000)
        command_latency = round(
            (t.created_at - ctx.message.created_at).total_seconds() * 1000
        )

        if ctx.voice_client:
            voice_latency = round(ctx.voice_client.ping)
        else:
            voice_latency = "N/A"

        embed = PingEmbed(bot_latency, command_latency, voice_latency)
        await t.edit(content="", embed=embed)


async def setup(bot):
    await bot.add_cog(Ping(bot))
    log.info("Module loaded")
