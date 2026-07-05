from ast import alias
from encodings import aliases
import logging
from discord.ext import commands

from Replies.Strings import Messages

from Suica import Bot

log = logging.getLogger(__name__)

class FeatureFlagManager(commands.Cog):
	
	def __init__(self, bot: Bot):
		self.bot = bot

	@commands.is_owner()
	@commands.command(name='flags', aliases=['fl'])
	async def _flags(self, ctx: commands.Context):
		"""
		List all the flags!
		"""

		await ctx.typing()

		flags = self.bot.feature_flags.list_all()

		if not flags:
			await ctx.message.add_reaction('🈳')
			return
		
		lines = []
		for flag, enabled in flags.items():
			status = '⭕' if enabled else '❌'
			lines.append(f"{flag} : {status}")

		await ctx.send(f'\n'.join(lines))

	@commands.is_owner()
	@commands.command(name='flagon', aliases=['flon', 'fon', 'on'])
	async def _flag_on(self, ctx: commands.Context, flag: str):
		"""
		Enable a flag
		"""
		if self.bot.feature_flags.enable(flag):
			await ctx.send(Messages.FEATURE_FLAG_ON.format(flag))
		else:
			await ctx.send(Messages.FEATURE_FLAG_NOT_FOUND.format(flag))

	@commands.is_owner()
	@commands.command(name='flagoff', aliases=['floff', 'foff', 'off'])
	async def _flag_off(self, ctx: commands.Context, flag: str):
		"""
		Disable a flag
		"""
		if self.bot.feature_flags.disable(flag):
			await ctx.send(Messages.FEATURE_FLAG_OFF.format(flag))
		else:
			await ctx.send(Messages.FEATURE_FLAG_NOT_FOUND.format(flag))

	# @commands.is_owner()
	@commands.command(name='flagtoggle', aliases=['fltoggle', 'ftoggle', 'toggle', 'tog'])
	async def _flag_toggle(self, ctx: commands.Context, flag: str):
		"""
		Toggle a flag
		"""
		new_flag_state = self.bot.feature_flags.toggle(flag)

		if new_flag_state is None:
			await ctx.send(Messages.FEATURE_FLAG_NOT_FOUND.format(flag))
		else:
			if new_flag_state == True:
				await ctx.send(Messages.FEATURE_FLAG_ON.format(flag))
			else:
				await ctx.send(Messages.FEATURE_FLAG_OFF.format(flag))
	
async def setup(bot: Bot):
	await bot.add_cog(FeatureFlagManager(bot))
	log.info("Module loaded")
       
	
	  