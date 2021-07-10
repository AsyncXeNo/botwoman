#!venv/bin/python3

import sys
import os

from dotenv import load_dotenv
from client import client

load_dotenv()
sys.path.append(os.getcwd())

if __name__ == '__main__':
	TOKEN = os.getenv('DISCORD_TOKEN')
	
	client.load_extension('cogs.debug')
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			if not filename[:-3] == "debug":
				client.load_extension(f'cogs.{filename[:-3]}')

	client.run(TOKEN)
