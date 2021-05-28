from datetime import timedelta
import discord
import logging
import os

from discord.ext import commands
from utils import Logger
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

BESTGUILD = os.getenv('BEST_GUILD')

customlogger = Logger('client.py')


# bot
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
	customlogger.log_neutral('Logged in as {0}!'.format(client.user))
	guild = discord.utils.find(lambda g: g.name == BESTGUILD, client.guilds)
	customlogger.log_neutral(
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name} (id: {guild.id})'
	)


# @client.event
# async def on_message(message):
# 	customlogger.log_neutral('(#{0.channel}) {0.author}: {0.content}'.format(message))
# 	if message.author == client.user:
# 		return
# 	if message.content.split(' ')[0] == ('{0}ping'.format(client.get_prefix())):
# 		await message.channel.send('pong')


@client.command(description='Unmutes the specified user.')
@commands.is_owner()
async def unmute(ctx, member: discord.Member):
	muterole = discord.utils.find(lambda g: g.name == 'Muted', ctx.guild.roles)
	await member.remove_roles(muterole)
	await ctx.send('Unmuted {0}.'.format(member.mention))


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
		

@client.event
async def on_error(event, *args, **kwargs):
	with open('err.log', 'a') as f:
		if event == 'on_message':
			customlogger.log_alert('Error logged to err.log')
			f.write(f'Unhandled message: {args[0]}\n')
		else:
			raise Exception
