#!venv/bin/python3

import sys
import os

from dotenv import load_dotenv
from client import client, load_ext, unload_ext

load_dotenv()
sys.path.append(os.getcwd())

if __name__ == '__main__':
	TOKEN = os.getenv('DISCORD_TOKEN')
	
	load_ext('debug')
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py') and not filename.startswith('debug'):
			load_ext(filename[:-3])

	client.run(TOKEN)