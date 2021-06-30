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

        custom_nsfw = [
            "gräfenberg spot",
            "shotacon",
            "shota",
            "male genitalia",
            "female genitalia",
            "cyclopia"
        ]

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

        if profanity.contains_profanity(query) or query.lower() in custom_nsfw:
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

        image_index = None

        for image in results.images:
            if "thumb" in image.lower() or "cover" in image.lower() or "main" in image.lower():
                image_index = results.images.index(image)

        if image_index == None:
            image_index = 3 if len(results.images) >= 4 else len(results.images) -1
            
        embed.set_image(url=results.images[image_index])

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Utils(client))
