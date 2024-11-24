import discord
from discord import Webhook
from discord.ext import commands
import asyncio, urllib.request
import os, io, textwrap, inspect
import aiohttp
from contextlib import redirect_stdout
import traceback


from discord import Webhook




class Owner(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self._last_result = None
		self.sessions = set()

	def clean_code(self,content):
		if content.startswith("```") and content.endswith("```"):
			return "\n".join(content.split('\n')[1:-1])
	
	def get_syntax_error(self, e):
		if e.text is None:
			return f'```py\n{e.__class__.__name__}: {e}\n```'
		return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'
	
	@commands.command(description="Enable or disable command", hidden=True)
	@commands.is_owner()
	async def toggle(self,ctx, *, command):
		command = self.bot.get_command(command)

		if command is None:
			await ctx.send("I can't find the command")

		elif ctx.command == command:
			await ctx.send("You can't disable the command")
		
		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			await ctx.send(f"I have {ternary} {command.qualified_name}")

	@commands.command(hidden=True)
	@commands.is_owner()
	async def changeav(self,ctx, pic:discord.Attachment):
		if pic.size > 8388608:
			await ctx.send('File is too big')
		if pic.size <= 8388608:
			await self.bot.user.edit(avatar=pic.read())
			await ctx.send('The pfp is changed')
		if pic == None:
			await ctx.send('You have to put an image as your attachment')


	@commands.command(hidden=True)
	@commands.is_owner()
	async def reset(self,ctx,command):
		commands = self.bot.get_command(command)
		commands.reset_cooldown(ctx)
		await ctx.send(f'Done, cooldown on {command} has been reset!')


	@commands.command(hidden=True)
	@commands.is_owner()
	async def edit(self,ctx,message_id:int,*,message):
		msg = await ctx.fetch_message(message_id)
		await msg.edit(content=message)
	



	@commands.command(hidden=True)
	@commands.is_owner()
	async def off(self,ctx):
		await ctx.send("Bot is turning off")
		await self.bot.close()
		await ctx.send("Failed")

	@commands.command(hidden=True)
	@commands.is_owner()
	async def say(self,ctx,*,message):
		await ctx.message.delete()
		await ctx.send(f'{message}')
	
	@commands.command(hidden=True,name='eval')
	@commands.is_owner()
	async def _eval(self, ctx, *, body: str):
		"""Evaluates a code"""
		try:
			env = {
				'bot': self.bot,
				'ctx': ctx,
				'channel': ctx.channel,
				'author': ctx.author,
				'guild': ctx.guild,
				'message': ctx.message,
				'_': self._last_result
					}

			env.update(globals())

			body = self.clean_code(body)
			stdout = io.StringIO()

			to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

			try:
				exec(to_compile, env)
			except Exception as e:
				return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

			func = env['func']
			try:
				with redirect_stdout(stdout):
					ret = await func()
			except Exception as e:
				value = stdout.getvalue()
				await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
			else:
				value = stdout.getvalue()
				try:
					await ctx.message.add_reaction('\u2705')
				except:
					pass

					if ret is None:
						if value:
							await ctx.send(f'```py\n{value}\n```')
					else:
						self._last_result = ret
						await ctx.send(f'```py\n{value}{ret}\n```')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

	@commands.command(name='repl', hidden=True)
	@commands.is_owner()
	async def _repl(self,ctx):
		variables = {
			'bot': self.bot,
			'ctx': ctx,
			'channel': ctx.channel,
			'author': ctx.author,
			'guild': ctx.guild,
			'message': ctx.message,
			'_': self._last_result
		}
		try:
			if ctx.channel.id in self.sessions:
				await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
				return
			self.sessions.add(ctx.channel.id)
			await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')

			def check(m):
				return m.author.id == ctx.author.id and \
				m.channel.id == ctx.channel.id and \
				m.content.startswith('`')
			while True:
				try:
					response = await self.bot.wait_for('message', check=check, timeout=10.0 * 60.0)
				except asyncio.TimeoutError:
					await ctx.send('Exiting REPL session.')
					self.sessions.remove(ctx.channel.id)
					break
				cleaned = self.clean_code(response.content)

				if cleaned in ('quit', 'exit', 'exit()'):
					await ctx.send('Exiting.')
					self.sessions.remove(ctx.channel.id)
					return
				executor = exec
				if cleaned.count('\n') == 0:
					try:
						code = compile(cleaned, '<repl session>', 'eval')
					except SyntaxError:
						pass
					else:
						executor = eval
				if executor is exec:
					try:
						code = compile(cleaned, '<repl session>', 'exec')
					except SyntaxError as e:
						await ctx.send(self.get_syntax_error(e))
						continue
					
				variables['message'] = response
				fmt = None
				stdout = io.StringIO()
				try:
					with redirect_stdout(stdout):
						result = executor(code, variables)
						if inspect.isawaitable(result):
							result = await result
				except Exception as e:
					value = stdout.getvalue()
					fmt = f'```py\n{value}{traceback.format_exc()}\n```'
				else:
					value = stdout.getvalue()
					if result is not None:
						fmt = f'```py\n{value}{result}\n```'
						variables['_'] = result
					elif value:
						fmt = f'```py\n{value}\n```'
				try:
					if fmt is not None:
						if len(fmt) > 2000:
							await ctx.send('Content too big to be printed.')
						else:
							await ctx.send(fmt)
				except discord.Forbidden:
					pass
				except discord.HTTPException as e:
					await ctx.send(f'Unexpected error: `{e}`')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')


	@commands.command(name='smalleval')
	@commands.is_owner()
	async def small(self,ctx,command:str):
		res = eval(command)
		await ctx.send(await res)

	@commands.command(hidden=True)
	@commands.is_owner()
	async def load(self,ctx,*,extension):
		if extension == ctx.cog:
			await ctx.send('I don\'t think thats possible')
		elif extension != ctx.cog:
			try:
				await self.bot.load_extension(f'commands.{extension}')
				await ctx.send('Loaded')
			except Exception as e:
				await ctx.send(f'{type(e).__name__}: {e}')

	
	@commands.command(hidden=True)
	@commands.is_owner()
	async def unload(self,ctx,*,extension):
		if extension == ctx.cog:
			await ctx.send('I don\'t think thats possible')
		elif extension != ctx.cog:
			try:
				await self.bot.unload_extension(f'commands.{extension}')
				await ctx.send('Unloaded')
			except Exception as e:
				await ctx.send(f'{type(e).__name__}: {e}')
	@commands.command(hidden=True)
	@commands.is_owner()
	async def reload(self,ctx,*,extension):
		if extension == ctx.cog:
			await ctx.send('I don\'t think thats possible')
		elif extension != ctx.cog:
			try:
				await self.bot.unload_extension(f'commands.{extension}')
				await 	self.bot.load_extension(f'commands.{extension}')
				await ctx.send('Reloaded')
			except Exception as e:
				await ctx.send(f'{type(e).__name__}: {e}')
		
	@commands.group(name='object',aliases=['obj'], invoke_without_command=True)
	@commands.is_owner()
	async def object(self,ctx):
		return
	@object.command(name='member')
	@commands.is_owner()
	async def member(self,ctx,x):
		member = discord.Object(id=x)	
		try:
			embed=discord.Embed(title=f'{member.display_name}\'s avatar', description="")
			embed.set_image(url=f'{member.avatar_url}')
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')
	

	
	@commands.group(name='bot',invoke_without_command=True)
	@commands.is_owner()
	async def botinfo(self,ctx):
		embed = discord.Embed(title='Bot Info',description=f'**Bot version**: {discord.__version__}\n**Amount of Commands**: {len(self.bot.commands)}\n**Amount of Category**: {len(self.bot.cogs)}\n**Guilds**: {len(self.bot.guilds)}')
		await ctx.send(embed=embed)
	
	@botinfo.command(name='avatar')
	@commands.is_owner()
	async def changeavatar(self,ctx,link=None):
		try:
			if link == None:
				file = ctx.message.attachments[0]
				await file.save(f'./assets/avatar.{file.filename[-3:]}')
				with open(f'./assets/avatar.{file.filename[-3:]}', 'rb') as f:
					img = f.read()
				await self.bot.user.edit(avatar=img)
				await ctx.send('Changed the avatar')
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')

	@commands.command(name='createembed',aliases=['ce'])
	@commands.is_owner()
	async def createembed(self,ctx,*,code):
		try:
			embed=discord.Embed.from_dict(dict(code))
			await ctx.send(embed=embed)
		except Exception as e:
			await ctx.send(f'{type(e).__name__}: {e}')


async def setup(bot):
	await bot.add_cog(Owner(bot))
