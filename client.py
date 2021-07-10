from datetime import timedelta
import discord
import asyncio
import logging
import os
import json

from discord.ext import commands
from utils.logger import Logger
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

BESTGUILD = os.getenv('BEST_GUILD')
DEBUGCHANNEL = 851344906185343016

customlogger = Logger('client')


# bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)

with open("data/logs.json", "w") as f:
	json.dump([], f)



@client.event
async def on_ready():
	customlogger.log_neutral('Logged in as {0}!'.format(client.user))


# @client.event
# async def on_command_error(ctx, error):
# 	channel = client.get_channel(DEBUGCHANNEL)
# 	await channel.send('```{0}```'.format(error))


# @client.event
# async def on_message(message):
# 	customlogger.log_neutral('(#{0.channel}) {0.author}: {0.content}'.format(message))
# 	if message.author == client.user:
# 		return
# 	if message.content.split(' ')[0] == ('{0}ping'.format(client.get_prefix())):
# 		await message.channel.send('pong')

@client.command(description="ban")
@commands.is_owner()
async def ban(ctx, member: discord.Member):
	await ctx.send(f"React to this message with :thumbsup: to vote for banning {member.name}. He will be banned once this message reaches 5 reactions")

	def check(reaction, user):
		return str(reaction.emoji) == '👍'

	reactions = 0 

	while not reactions == 5:
		try:
			reaction, user = await client.wait_for("reaction_add", timeout=60.0, check=check)
		except asyncio.TimeoutError:
			await ctx.send(f"No reaction for the past 60 seconds. Guess {member.name} is not banned.")
			return
		
		reactions += 1
		await ctx.send(reactions)

	await member.kick(reason="being a pedo")
	await ctx.send(f"Banned {member.name}")

	customlogger.log_neutral(f"kicked {member.name}")
			

@client.command(description='Unmutes the specified user.')
@commands.is_owner()
async def unmute(ctx, member: discord.Member):
	muterole = discord.utils.find(lambda g: g.name == 'Muted', ctx.guild.roles)
	await member.remove_roles(muterole)
	await ctx.send('Unmuted {0}.'.format(member.mention))
	customlogger.log_neutral('Unmuted {0}.'.format(member.name))


@client.command(description="Mutes the specified user.")
@commands.is_owner()
async def mute(ctx, member: discord.Member, *, reason=None):
	guild = ctx.guild
	muterole = discord.utils.find(lambda g: g.name == 'Muted', ctx.guild.roles)

	if not muterole:
		customlogger.log_error('make a mute role dumbass\nExiting program...')
		return

	await ctx.send('{0} was muted.'.format(member.mention))
	await member.add_roles(muterole, reason=reason)
	customlogger.log_neutral('Muted {0}.'.format(member.name))


@client.command(description='Pings the bot.')
async def ping(ctx):
	await ctx.send(f"{int(client.latency*1000)} ms")


@client.command(description="Gets your avatar.", aliases=["av"])
async def avatar(ctx, member:discord.Member = None):
	if member:
		url = member.avatar_url
	else:
		url = ctx.author.avatar_url
	
	await ctx.send(url)


@client.command(description="you do not need to know")
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')
	await ctx.send("ok")


@client.command(description="you do not need to know")
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	await ctx.send("ok")
	customlogger.log_neutral(f"Unloaded {extension}")


@client.command(description="you do not need to know")
@commands.is_owner()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	customlogger.log_neutral(f"Unloaded {extension}")
	client.load_extension(f'cogs.{extension}')
	await ctx.send("ok")
