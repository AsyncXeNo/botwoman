import discord
import sys
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def selfdestruct(self, ctx):
        await ctx.send('I\'m done with life.')
        sys.exit()


def setup(client):
    client.add_cog(Utils(client))