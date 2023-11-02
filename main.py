from discord.ext import commands
import discord

import asyncio
import logging
import pkgutil

import Extensions

# root logger setup
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# In 2.0 the intents are required
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_extensions():
    # load every extension in the Extensions package
    for _, name, _ in pkgutil.iter_modules(Extensions.__path__):
        try:
            await bot.load_extension("Extensions." + name)
        except Exception as e:
            log.error("Failed to load extension {}: {}".format(name, e))


asyncio.run(load_extensions())

# TODO: Revive config function and hide tokens in config.json (and change the token before making this repo public)
bot.run("NTgyNDUzNzAzNzYwNDEyNjcz.GuZDnn.MuEpoM-xtUOpnbfEmJOPnmm2mmocrZBDrjzVfQ")
