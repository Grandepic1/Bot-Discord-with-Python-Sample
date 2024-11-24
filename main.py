import discord
import os
import asyncio
from discord.ext import commands
import nest_asyncio
from dotenv import load_dotenv
nest_asyncio.apply()
load_dotenv()



bot = commands.Bot(
	command_prefix=os.getenv("PREFIX"),
	case_insensitive=True,
	owner_ids=[put your discord id here],
	intents=discord.Intents.all(),
)

async def load_extension():
	for filename in os.listdir('commands'):
		if filename.endswith('.py'):
			await bot.load_extension(f'commands.{filename[:-3]}')

async def main():
#	keep_alive()
	await load_extension()
	bot.run(os.getenv('TOKEN'))

asyncio.run(main())
