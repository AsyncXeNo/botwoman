#!venv/bin/python3

import sys
import os

from dotenv import load_dotenv
from client import client

load_dotenv()
sys.path.append(os.getcwd())

if __name__ == '__main__':
	TOKEN = os.getenv('DISCORD_TOKEN')
	client.run(TOKEN)
