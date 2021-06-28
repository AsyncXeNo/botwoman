import discord
import sys
from discord.ext import commands

import wikipedia

wikipedia.set_lang("en")


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Searches wikipedia for the given query.")
    async def wiki(self, ctx, *args):
        query = " ".join(args)
        try:
            results = wikipedia.page(query, auto_suggest=False, redirect=True)
        except wikipedia.exceptions.DisambiguationError as e:
            await ctx.send("\n".join(e.options))
            return
        except wikipedia.exceptions.PageError as e:
            await ctx.send("An article for this query doesn't exist.")
            return

        response = results.summary.split("\n")[0]

        embed = discord.Embed(
            title=query.title(), 
            url=results.url, 
            description=response
        )

        embed.set_image(url=results.images[1])

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Utils(client))
