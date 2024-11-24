import os

import discord
import asyncio
from discord.ext import commands
import random

Random_colors = random.sample(range(0, 999999), 100)

class Moderation(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
	@commands.command(help="Ban members")
	@commands.has_permissions(ban_members=True)
	@commands.guild_only()
	async def ban(self,ctx,member : discord.Member,*,reason="No reason provided"):
		await ctx.send(f"**{member.name}** has been banned from the server because {reason}")
		await member.send(f'You have been banned from {ctx.guild.name}. reason={reason}')
		await asyncio.sleep(0.5)
		await member.ban(reason=reason)

	@commands.command(help="Kick members")
	@commands.has_permissions(kick_members=True)
	@commands.guild_only()
	async def kick(self,ctx,member : discord.Member,*,reason="No reason provided"):
		await ctx.send(f"**{member.name}** has been kicked from the server because {reason}")
		await member.send(f'You have been kicked from {ctx.guild.name}. reason={reason}')
		await asyncio.sleep(0.5)
		await member.kick(reason=reason)	

	@commands.command(help="Mute members")
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def mute(self,ctx, member: discord.Member ,*, reason=None):
		guild = ctx.guild
		channel = self.bot.get_channel(os.getenv('ROLE-MUTE'))
		role = discord.utils.get(guild.roles, name="Criminal")
		await ctx.send(f'**{member.name}** is the new CRIMINAL!')
		await member.add_roles(role)
		await asyncio.sleep(2)
		await channel.send(f'{member.mention}, Welcome new CRIMINAL! you just got muted because `{reason}`. Ping a mod if you think you didn\'t do something wrong')

	@commands.command(help="Mute many members")
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def massmute(self,ctx,*members:discord.Member):
		role = ctx.guild.get_role(os.getenv('ROLE-MUTE'))
		await asyncio.sleep(1)
		for member in members:
			await member.add_roles(role)
		await ctx.send('Muted.')

	@commands.command(help="Unmute members")
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def unmute(self,ctx, member: discord.Member):
		guild = ctx.guild
		role = ctx.guild.get_role(os.getenv('ROLE-MUTE'))
		await ctx.send(f'**{member.name}** is not a muted anymore')
		await member.remove_roles(role)
	
	@ban.error
	async def ban_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Mention an account to be banned")
		if isinstance(error, commands.BadArgument):
			await ctx.send("Mention an account to be banned")
	
	@unmute.error
	async def unmute_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Mention an account to be unmuted")
		if isinstance(error, commands.BadArgument):
			await ctx.send("Mention an account to be unmuted")
	
	@kick.error
	async def kick_error(self,ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Mention an account to be kicked from the server")
		if isinstance(error, commands.BadArgument):
			await ctx.send("Mention an account to be kicked from the server")

	@mute.error
	async def mute_error(self,ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Mention an account to be muted")
		if isinstance(error, commands.BadArgument):
			await ctx.send("Mention an account to be muted")


	@commands.command(help='Lock server')
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def lock(self, ctx):
		guild = ctx.guild
		permissions = discord.Permissions()
		permissions.update(read_messages=True)
		role = discord.utils.get(guild.roles, name="citizens")
		await role.edit(reason=None, permissions=permissions)
		await ctx.send('Locked the server')
	
	@commands.command(help='Unlock the sever')
	@commands.has_permissions(manage_guild=True)
	@commands.guild_only()
	async def unlock(self,ctx):
		guild = ctx.guild
		permissions = discord.Permissions()
		permissions.update(read_messages=True, add_reactions=True, attach_files=True, change_nickname=True, connect=True, create_instant_invite=True, embed_links=True, external_emojis=True, read_message_history=True, request_to_speak=True, send_messages=True, speak=True, stream=True, use_external_emojis=True, use_voice_activation=True)
		role = discord.utils.get(guild.roles, name="citizens")
		await role.edit(reason=None, permissions=permissions)
		await ctx.send('Unlocked the server')


	
async def setup(bot):
	await bot.add_cog(Moderation(bot))