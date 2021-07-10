import discord
from discord.ext import commands
from utils.logger import Logger
from dotenv import load_dotenv

load_dotenv()


class Debug(commands.Cog):
    async def __init__(self, client):
        self.logger = Logger("cogs/debug")
        await Logger.subscribe(self)

        self.client = client

        self.DEBUG_CHANNEL = self.client.get_channel(851344906185343016)

    async def logger_event(self, post):
        await self.DEBUG_CHANNEL.send(f"```{post}```")


async def setup(client):
    await client.add_cog(Debug(client))