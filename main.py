from discord.ext import commands

import asyncio
import logging

import Suica  # Custom bot class

# root logger setup
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

bot = Suica.Bot()

asyncio.run(bot.load_extensions())

bot.run(bot.token)
