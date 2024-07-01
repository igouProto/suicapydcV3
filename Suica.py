import json
import discord
import logging
import pkgutil
from discord.ext import commands

import Extensions
from Replies.Strings import Messages

log = logging.getLogger(__name__)

"""
The main bot class that inherits from commands.Bot. It's responsible for loading extensions and setting up itself.
"""


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        """
        The bot's token, prefix, and backstage channel are set here.
        Typically it loads configuration from config.json, 
        but if it's not found, it will prompt the user to enter the required information.
        """
        self.token = ""
        self.backstage_channel = None
        self.prefix = "."
        self.version = "3.1.2"
        self.status_message = ""

        # Load configuration from config.json
        try:
            with open("Assets/config.json", "r") as source:
                config = json.load(source)
                log.info("Config loaded from Assets/config.json")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # if config.json is not found, treat it as a fresh setup
            log.error(
                "Failed to load config.json: {}, starting initial setup".format(e)
            )
            token = input("Enter bot token: ")
            prefix = input("Enter command prefix: ")
            backstage_channel = input("Enter backstage channel ID: ")
            # save configuration
            config = {
                "token": token,
                "prefix": prefix,
                "backstage_channel": backstage_channel,
            }
            with open("Assets/config.json", "w") as target:
                json.dump(config, target)
                log.info(
                    "Config saved to Assets/config.json and will be loaded on next startup"
                )

        # Setup intents as they are required in 2.0
        intents = discord.Intents.default()
        intents.message_content = True

        # Init the bot after setting the token and prefix
        self.token = config["token"]
        self.prefix = config["prefix"]
        self.backstage_channel = config["backstage_channel"]
        self.status_message = Messages.DEFAULT_STATUS_MESSAGE.format(
            self.version, self.prefix
        )
        super().__init__(command_prefix=self.prefix, intents=intents)

    async def load_extensions(self):
        """
        Loads all extensions in the Extensions folder.
        """
        log.info("Loading extensions...")
        for _, name, _ in pkgutil.iter_modules(Extensions.__path__):
            try:
                await self.load_extension("Extensions." + name)
            except Exception as e:
                log.error("Failed to load extension {}: {}".format(name, e))
        log.info("Extensions loaded")
