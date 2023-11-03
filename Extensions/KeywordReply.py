import logging
from discord.ext import commands
from Replies.Messages import Messages

# logging
log = logging.getLogger(__name__)

'''
Keyword reply function!
'''

class KeywordReply(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # container for keyword-reply pairs
        self.dictionary = {}

        # blacklisted guilds in case some wants to turn this off
        self.blacklist = []

        #load the raw keyword-reply pairs from the file
        try:
            with open('Assets/keywords.txt', 'r') as source:
                for line in source:
                    (keyword, reply) = line.split(':', 1)
                    self.dictionary[keyword] = reply
            source.close()
            log.info("Loaded keyword pairs from keywords.txt")
        except Exception as e:
            log.error("Failed to load keywords.txt: {}".format(e))

    # main reply function
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild.id in self.blacklist:
            return

        if message.content in self.dictionary.keys():
            await message.channel.send(self.dictionary[message.content])

    # reply function toggle
    @commands.command(name="togglekw")
    async def _toggle_kw(self, ctx):
        if ctx.guild.id in self.blacklist:
            self.blacklist.remove(ctx.guild.id)
            await ctx.send(Messages.KEYWORD_REPLY_ENABLED.format(ctx.guild.name))
        else:
            self.blacklist.append(ctx.guild.id)
            await ctx.send(Messages.KEYWORD_REPLY_DISABLED.format(ctx.guild.name))

    # add a keyword-reply pair and write to keywords.txt
    @commands.command(name="addkw")
    async def _add_kw(self, ctx, keyword, reply):
        if keyword in self.dictionary.keys():
            await ctx.send(Messages.KEYWORD_KEY_EXISTS)
            return

        self.dictionary[keyword] = reply

        try:
            with open('Assets/keywords.txt', 'a') as source:
                source.write("\n{}:{}".format(keyword, reply))
            source.close()
        except Exception as e:
            log.error("Failed to write to keywords.txt: {}".format(e))

        await ctx.send(Messages.KEYWORD_REPLY_ADDED + "`{}: {}`".format(keyword, reply))

    # remove a keyword-reply pair and write to keywords.txt
    @commands.command(name="rmkw")
    async def _remove_kw(self, ctx, key):
        if key in self.dictionary.keys():
            self.dictionary.pop(key)
            await ctx.send(Messages.KEYWORD_REPLY_REMOVED + "`{}`".format(key))

            # completely rewrite keywords.txt
            try:
                with open('Assets/keywords.txt', 'w') as source:
                    for key in self.dictionary.keys():
                        source.write("{}:{}".format(key, self.dictionary[key]))
                source.close()
            except Exception as e:
                log.error("Failed to write to keywords.txt: {}".format(e))

        else:
            await ctx.send(Messages.KEYWORD_KEY_NOT_FOUND)
        

async def setup(bot):
    await bot.add_cog(KeywordReply(bot))
    log.info("Module loaded")