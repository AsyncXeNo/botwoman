import discord
from discord.ext import commands, tasks
from utils.logger import Logger
from dotenv import load_dotenv

load_dotenv()


class Debug(commands.Cog):
    def __init__(self, client):
        self.logger = Logger("cogs/debug")

        self.client = client
        self.logs = []
        self.DEBUGCHANNEL = 851344906185343016

        Logger.subscribe(self)
        self.logger.log_neutral("Loaded debug")

        self.started = False

    def logger_event(self, log):
        self.logs.append(log)

    @tasks.loop(seconds=0.5)
    async def post_log(self):
        if not len(self.logs) == 0:
            channel = self.client.get_channel(self.DEBUGCHANNEL)
            msg = self.logs.pop(0)
            await channel.send(f"`{msg}`")


def setup(client):
    client.add_cog(Debug(client))