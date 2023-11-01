from discord.ext import commands

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
        except Exception as e:
            print(e)
            print("Error loading keywords.txt")

    # main reply function
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.guild.id in self.blacklist:
            return

        if message.content in self.dictionary.keys():
            await message.channel.send(self.dictionary[message.content])

    # toggle the function on and off by adding or removing the guild from the blacklist
    @commands.command(name="togglekw")
    async def _toggle_kw(self, ctx):
        if ctx.guild.id in self.blacklist:
            self.blacklist.remove(ctx.guild.id)
            await ctx.send("已開啟關鍵字回覆")
        else:
            self.blacklist.append(ctx.guild.id)
            await ctx.send("已關閉關鍵字回覆")
        

async def setup(bot):
    await bot.add_cog(KeywordReply(bot))
    print("Keyword reply loaded")