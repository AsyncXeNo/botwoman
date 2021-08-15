from logging import log
import os
import discord

from discord.ext import commands, tasks
from utils.my_logging import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)


class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.started = False

    @tasks.loop(seconds=0.5)
    async def post_log(self):
        self.DEBUGCHANNEL = self.client.get_channel(851344906185343016)
        counter = 0
        async for _ in self.DEBUGCHANNEL.history(limit=3):
            counter += 1
        if counter < 1:
            await self.DEBUGCHANNEL.send('Initializing...')
            self.message = await self.DEBUGCHANNEL.fetch_message(self.DEBUGCHANNEL.last_message_id)
        
        with open('logs/debug.log', 'r') as f:
            logs = f.read()
        if self.message.content.strip('```') != logs: await self.message.edit(content=f'```{logs}```')


def setup(client):
    client.add_cog(Debug(client))