import discord
import asyncio
import logging
import os
import json

from discord.ext import commands
from utils.my_logging import get_logger
from dotenv import load_dotenv

load_dotenv()

d_logger = logging.getLogger('discord')
d_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
d_logger.addHandler(handler)

logger = get_logger(__name__)

BESTGUILD = os.getenv('BEST_GUILD')
DEBUGCHANNEL = int(os.getenv('DEBUG_CHANNEL'))

# bot
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix='!', intents=intents)


def load_ext(extension):
	client.load_extension(f'cogs.{extension}')
	logger.info(f'Loaded {extension}.')


def unload_ext(extension):
	client.unload_extension(f'cogs.{extension}')
	logger.info(f'Unloaded {extension}.')


@client.event
async def on_ready():
	logger.info('Logged in as {0}!'.format(client.user))
	await client.get_channel(DEBUGCHANNEL).purge(limit=10000)
	client.get_cog("Debug").post_log.start()