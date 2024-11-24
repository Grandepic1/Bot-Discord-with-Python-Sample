from discord.ext import commands


class event(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
		self._cd = commands.CooldownMapping.from_cooldown(1, 60*2*60, commands.BucketType.guild)

	@commands.Cog.listener()
	async def on_ready(self):
		print("The bot is active")



		
	@commands.Cog.listener()
	async def on_command_error(self,ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			if error.retry_after < 60:
				await ctx.send('**Still in cooldown**, please wait `{:.0f}` seconds'.format(error.retry_after%60))
			elif error.retry_after >= 60:
				await ctx.send('**Still in cooldown**, please wait `{:.0f}` minutes `{:.0f}` seconds'.format(error.retry_after//60, error.retry_after%60))
			elif error.retry_after >= 3600:
				await ctx.send('**Still in cooldown**, please wait `{:.0f}` hours `{:.0f}` minutes `{:.0f}`'.format(error.retry_after//3600, error.retry_after//60, error.retry_after%60))
		if isinstance(error, commands.CommandNotFound):
			await ctx.send("You sure that command is available? Or you are too smart to make typos?")
		if isinstance(error, commands.DisabledCommand):
			await ctx.send("Command is disabled by the owner. RIP")
		if isinstance(error, commands.MissingPermissions):
			await ctx.send(f"You don't have the {error.missing_perms} permissions to run `{ctx.command.name}`, buddy")
		if isinstance(error, commands.NotOwner):
			await ctx.send("Who tf are you?! You are not my owner!")
		if isinstance(error, commands.MemberNotFound):
			argument = await commands.clean_content().convert(ctx, error.argument)
			await ctx.send(f'Can\'t find {argument}')
		if isinstance(error, commands.ChannelNotFound):
			argument = await commands.clean_content().convert(ctx, error.argument)
			await ctx.send(f'Can\'t find {argument}')
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.send(f'Can\'t execute the command. Bot doesn\'t have {error.missing_perms} permissions')
		if isinstance(error, commands.MissingRole):
			role = ctx.guild.get_role(error.missing_role)
			await ctx.send(f'You don\'t have {role.name} role')
		if isinstance(error, commands.NoPrivateMessage):
			await ctx.send('You can\'t run this command in DM!')
		if isinstance(error, commands.PrivateMessageOnly):
			await ctx.send("You only can run this command in DM!")
		"""if isinstance(error, commands.CheckFailure):
			await ctx.send('You are blacklisted sadly', delete_after=5)"""
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f'Required agument for this command:\n```\n{ctx.prefix}{ctx.command.name} {" ".join(list(ctx.command.clean_params)[len(ctx.args[2:] if ctx.command.cog else ctx.args[1:])])}\n```')


	@commands.Cog.listener()
	async def on_message(self,msg):
		if msg.author.bot:
			return
		if msg.content.lower().startswith("hi"):
			await msg.channel.send("hello")

async def setup(bot):
	await bot.add_cog(event(bot))