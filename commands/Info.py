import discord
from discord.ext import commands



def rap_battle(ctx):
	return ctx.channel.id == 759626287173074974

class MyHelpCommand(commands.MinimalHelpCommand):
	async def send_pages(self):
		destination = self.get_destination()
		e = discord.Embed(title="Help Command", description='')
		for page in self.paginator.pages:
			e.description += page
		await destination.send(embed=e)


class Info(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self


	
	@commands.command(help="To find the latency of the bot")
	async def ping(self, ctx):
		await ctx.send(f'Pong!. `{round(self.bot.latency * 1000)}ms`')


	@commands.command(help="Show user's pfp", aliases=['av'])
	async def avatar(self, ctx, member: discord.Member=None):
		member = member or ctx.author
		embed=discord.Embed(title=f'{member.display_name}\'s avatar', description="")
		embed.set_image(url=f'{member.avatar_url}')
		await ctx.send(embed=embed)
	@commands.group(aliases=['server'],invoke_without_command=True)
	async def guild(self,ctx):
		return
	
	
	@guild.command()
	async def icon(self,ctx):
		guild = ctx.guild
		embed =discord.Embed(title=f'{guild.name}\'s icon')
		embed.set_image(url=guild.icon_url )
		await ctx.send(embed=embed)
		
async def setup(bot):
	await bot.add_cog(Info(bot))
