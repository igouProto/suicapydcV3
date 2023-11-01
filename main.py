from discord.ext import commands
import discord

# In 2.0 the intents are required
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '!', intents = intents)

bot.run("NTgyNDUzNzAzNzYwNDEyNjcz.GuZDnn.MuEpoM-xtUOpnbfEmJOPnmm2mmocrZBDrjzVfQ")

