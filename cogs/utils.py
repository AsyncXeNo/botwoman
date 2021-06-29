import discord
import sys
from discord.ext import commands

from better_profanity import profanity

import wikipedia

wikipedia.set_lang("en")


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Searches wikipedia for the given query.")
    async def wiki(self, ctx, *args):
        query = " ".join(args).lower()

        if query.lower() == "pizza":
            await ctx.send("Did you mean retard (Y/N)")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.client.wait_for("message", check=check)

            if not (msg.content.lower() in ["y", "n"]):
                await ctx.send("That was not an option (?)")
                return

            if msg.content.lower() == "y":
                query = "intellectual disability"
            else:
                query = "pizza"

        if profanity.contains_profanity(query):
            if not ctx.channel.is_nsfw():
                await ctx.send("You can only search that in NSFW channels.")
                return

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

        embed.set_image(url=results.images[3])

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Utils(client))
