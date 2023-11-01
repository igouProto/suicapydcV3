from discord.ext import commands
import discord
import asyncio
import Extensions

# In 2.0 the intents are required
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    await bot.load_extension("Extensions.BotManager")

asyncio.run(load_extensions())

# TODO: Revive config function and hide tokens in config.json
bot.run("NTgyNDUzNzAzNzYwNDEyNjcz.GuZDnn.MuEpoM-xtUOpnbfEmJOPnmm2mmocrZBDrjzVfQ")