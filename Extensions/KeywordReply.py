import logging
import discord
from discord.ext import commands
from Replies.Strings import Messages
import Suica

# logging
log = logging.getLogger(__name__)

"""
Keyword reply function!
Suica replies if it catches a keyword from chat.
Supports public and guild-specific dictionaries.
"""

# TODO: Refactor this pile of mess...


class KeywordReply(commands.Cog):
    def __init__(self, bot: Suica.Bot):
        """
        Initializes the public dictionary.
        """
        self.bot = bot

        # container for keyword-reply pairs
        self.public_dictionary = {}

        # container for guild-specific keyword-reply pairs
        self.guild_dictionaries = {}

        # blacklisted guilds in case some wants to turn this off
        self.blacklist = []

        # load the raw public keyword-reply pairs from the file
        log.info("Loading public keyword pairs from keywords.txt...")
        try:
            with open("Assets/keywords.txt", "r") as source:
                for line in source:
                    (keyword, reply) = line.split(":", 1)
                    self.public_dictionary[keyword] = reply
            source.close()
            log.info("Loaded keyword pairs from keywords.txt")
        except Exception as e:
            log.error("Failed to load keywords.txt: {}".format(e))
        log.info("Loaded {} keyword pairs".format(len(self.public_dictionary)))

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Loads the guild dictionaries when the bot is ready.
        """
        log.info("Loading keyword pairs for guilds...")
        # load every guild's keyword-reply pairs from the file
        for guild in self.bot.guilds:
            try:
                with open("Assets/keywords-{}.txt".format(guild.id), "r") as source:
                    self.guild_dictionaries[guild.id] = {}
                    for line in source:
                        try:
                            (keyword, reply) = line.split(":", 1)
                            self.guild_dictionaries[guild.id][keyword] = reply
                        except:
                            pass  # ignore lines that don't have a colon
                source.close()
                log.info(
                    "Loaded keyword pairs for guild {} ({})".format(
                        guild.name, guild.id
                    )
                )
            except Exception as e:
                log.error(
                    "Failed to load keyword pairs for guild {} ({}): {}".format(
                        guild.name, guild.id, e
                    )
                )

    # main reply function
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Checks if the message matches a keyword.
        The dictionary is checked in this order: public -> guild-specific.
        """
        if message.author.bot:
            return

        if message.guild.id in self.blacklist:
            return

        # look into the public dictionary first, then the guild's dictionary
        if message.content in self.public_dictionary.keys():
            await message.channel.send(self.public_dictionary[message.content])
        elif message.guild.id in self.guild_dictionaries.keys():
            if message.content in self.guild_dictionaries[message.guild.id].keys():
                await message.channel.send(
                    self.guild_dictionaries[message.guild.id][message.content]
                )

    # reply function toggle
    @commands.command(name="togglekw")
    async def _toggle_kw(self, ctx: commands.Context):
        """
        Toggles the keyword reply function for the guild in case someone wants to turn it off.
        """
        if ctx.guild.id in self.blacklist:
            self.blacklist.remove(ctx.guild.id)
            await ctx.send(Messages.KEYWORD_REPLY_ENABLED.format(ctx.guild.name))
        else:
            self.blacklist.append(ctx.guild.id)
            await ctx.send(Messages.KEYWORD_REPLY_DISABLED.format(ctx.guild.name))

    # add a keyword-reply pair to the public dictionary and write to keywords.txt
    @commands.command(name="addkwp")
    async def _add_kw(self, ctx: commands.Context, keyword, reply):
        """
        Adds a keyword-reply pair to the public dictionary.
        """
        if keyword in self.public_dictionary.keys():
            await ctx.send(Messages.KEYWORD_KEY_EXISTS)
            return

        self.public_dictionary[keyword] = reply

        Helpers.write_to_file(keyword=keyword, reply=reply)

        await ctx.send(Messages.KEYWORD_REPLY_ADDED + "`{}: {}`".format(keyword, reply))

    # remove a keyword-reply pair from the public dictionary and write to keywords.txt
    @commands.command(name="rmkwp")
    async def _remove_kw(self, ctx: commands.Context, key):
        """
        Removes a keyword-reply pair from the public dictionary.
        """
        if key in self.public_dictionary.keys():
            self.public_dictionary.pop(key)
            await ctx.send(Messages.KEYWORD_REPLY_REMOVED + "`{}`".format(key))

            # completely rewrite keywords.txt
            try:
                with open("Assets/keywords.txt", "w") as source:
                    for key in self.public_dictionary.keys():
                        source.write("{}:{}\n".format(key, self.public_dictionary[key]))
                source.close()
            except Exception as e:
                log.error("Failed to write to keywords.txt: {}".format(e))

        else:
            await ctx.send(Messages.KEYWORD_KEY_NOT_FOUND)

    # add a keyword-reply pair to the guild's dictionary and write to keywords-{guild.id}.txt
    @commands.command(name="addkw")
    async def _add_guild_kw(self, ctx: commands.Context, keyword, reply):
        """
        Adds a keyword-reply pair to the guild's dictionary.
        """
        # make a new dictionary for the guild if it doesn't exist
        if ctx.guild.id not in self.guild_dictionaries.keys():
            self.guild_dictionaries[ctx.guild.id] = {}

        if keyword in self.guild_dictionaries[ctx.guild.id].keys():
            await ctx.send(Messages.KEYWORD_KEY_EXISTS)
            return

        self.guild_dictionaries[ctx.guild.id][keyword] = reply

        Helpers.write_to_file(ctx.guild.id, keyword, reply)

        await ctx.send(Messages.KEYWORD_REPLY_ADDED + "`{}: {}`".format(keyword, reply))

    # remove a keyword-reply pair from the guild's dictionary and write to keywords-{guild.id}.txt
    @commands.command(name="rmkw")
    async def _remove_guild_kw(self, ctx: commands.Context, keyword):
        """
        Removes a keyword-reply pair from the guild's dictionary.
        """
        if ctx.guild.id in self.guild_dictionaries.keys():
            if keyword in self.guild_dictionaries[ctx.guild.id].keys():
                self.guild_dictionaries[ctx.guild.id].pop(keyword)
                await ctx.send(Messages.KEYWORD_REPLY_REMOVED + "`{}`".format(keyword))

                # completely rewrite keywords-{guild.id}.txt
                try:
                    with open(
                        "Assets/keywords-{}.txt".format(ctx.guild.id), "w"
                    ) as source:
                        for key in self.guild_dictionaries[ctx.guild.id].keys():
                            source.write(
                                "{}:{}\n".format(
                                    key, self.guild_dictionaries[ctx.guild.id][key]
                                )
                            )
                    source.close()
                except Exception as e:
                    log.error(
                        "Failed to write to keywords-{}.txt: {}".format(ctx.guild.id, e)
                    )

            else:
                await ctx.send(Messages.KEYWORD_KEY_NOT_FOUND)
        else:
            await ctx.send(Messages.KEYWORD_GUILD_NOT_FOUND.format(ctx.prefix))

    # backup the public dictionary to keywords.txt and send to chat
    @commands.is_owner()
    @commands.command(name="backupkwp")
    async def _backup_kw(self, ctx: commands.Context):
        """
        Exports the public dictionary to keywords.txt and sends it to chat.
        """
        try:
            await ctx.send(file=discord.File("Assets/keywords.txt"))
        except Exception as e:
            log.error(e)

    # backup the guild's dictionary to keywords-{guild.id}.txt and send to chat
    @commands.command(name="backupkw")
    async def _backup_guild_kw(self, ctx: commands.Context):
        """
        Send keywords-{guild.id}.txt to the chat.
        """
        if ctx.guild.id in self.guild_dictionaries.keys():
            try:
                await ctx.send(
                    file=discord.File("Assets/keywords-{}.txt".format(ctx.guild.id))
                )
            except Exception as e:
                log.error(e)
        else:
            await ctx.send(Messages.KEYWORD_GUILD_NOT_FOUND.format(ctx.prefix))

    # allow upload of keywords.txt and overwrite the public dictionary
    @commands.is_owner()  # uploading to the bot's directory is a bad idea...
    @commands.command(name="uploadkwp")
    async def _upload_kw(self, ctx: commands.Context):
        """
        Accepts a keywords.txt file and overwrites the public dictionary.
        This is made owner-only for security reasons.
        """
        if len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if attachment.filename == "keywords.txt":
                await attachment.save("Assets/keywords.txt")

                # load the raw public keyword-reply pairs from the file
                log.info("Loading public keyword pairs from keywords.txt...")
                try:
                    with open("Assets/keywords.txt", "r") as source:
                        for line in source:
                            (keyword, reply) = line.split(":", 1)
                            self.public_dictionary[keyword] = reply
                    source.close()
                    log.info("Loaded keyword pairs from keywords.txt")
                except Exception as e:
                    log.error("Failed to load keywords.txt: {}".format(e))
                log.info("Loaded {} keyword pairs".format(len(self.public_dictionary)))

                await ctx.send(Messages.KEYWORD_REPLY_RELOADED)
            else:
                await ctx.send(Messages.KEYWORD_REPLY_INVALID_FILE)
        else:
            await ctx.send(Messages.KEYWORD_REPLY_NO_FILE)

    # allow upload of keywords-{guild.id}.txt and overwrite the guild's dictionary
    @commands.is_owner()  # uploading to the bot's directory is a bad idea...
    @commands.command(name="uploadkw")
    async def _upload_guild_kw(self, ctx: commands.Context):
        """
        Accepts a keywords-{guild.id}.txt file and overwrites the guild's dictionary.
        Also made owner-only for security reasons.
        """
        guild_id = ctx.guild.id
        if len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if attachment.filename == "keywords.txt":
                await attachment.save("Assets/keywords-{}.txt".format(ctx.guild.id))

                # load this guild's keyword-reply pairs from the file
                try:
                    with open(
                        "Assets/keywords-{}.txt".format(ctx.guild.id), "r+"
                    ) as source:
                        self.guild_dictionaries[ctx.guild.id] = {}
                        for line in source:
                            (keyword, reply) = line.split(":", 1)
                            self.guild_dictionaries[ctx.guild.id][keyword] = reply

                        # before closing, see if there's a new line at the end of the file
                        # if not, add one so new entries don't get appended to the last line
                        source.seek(0)
                        last_char = source.read()[-1]
                        if last_char != "\n":
                            source.write("\n")

                    source.close()
                    log.info(
                        "Loaded keyword pairs for guild {} ({})".format(
                            ctx.guild.name, ctx.guild.id
                        )
                    )
                except Exception as e:
                    log.error(
                        "Failed to load keyword pairs for guild {} ({}): {}".format(
                            ctx.guild.name, ctx.guild.id, e
                        )
                    )
                log.info(
                    "Loaded {} keyword pairs for guild {}".format(
                        len(self.guild_dictionaries[ctx.guild.id]), ctx.guild.name
                    )
                )

                await ctx.send(Messages.KEYWORD_REPLY_RELOADED)
            else:
                await ctx.send(Messages.KEYWORD_REPLY_INVALID_FILE)
        else:
            await ctx.send(Messages.KEYWORD_REPLY_NO_FILE)


async def setup(bot):
    await bot.add_cog(KeywordReply(bot))
    log.info("Module loaded")


class Helpers:
    def write_to_file(guild_id=None, keyword=None, reply=None):
        """
        Writes a keyword-reply pair to file.
        """
        if not guild_id:
            file_name = "Assets/keywords.txt"
        elif guild_id:
            file_name = "Assets/keywords-{}.txt".format(guild_id)
        try:
            with open(file_name, "a") as source:
                source.write("{}:{}\n".format(keyword, reply))
            source.close()
        except Exception as e:
            # create a new file if it doesn't exist
            if isinstance(e, FileNotFoundError):
                with open(file_name, "w") as source:
                    source.write("{}:{}\n".format(keyword, reply))
                source.close()
            else:
                log.error("Failed to write to keywords-{}.txt: {}".format(guild_id, e))
