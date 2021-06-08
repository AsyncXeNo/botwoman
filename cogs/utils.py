import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def testing(self, ctx):
        await ctx.send('works.')


def setup(client):
    client.add_cog(Utils(client))