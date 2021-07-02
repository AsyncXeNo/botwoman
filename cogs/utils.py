import discord
import os
import sys
from discord.ext import commands

from google_images_search import GoogleImagesSearch

from better_profanity import profanity

from dotenv import load_dotenv

import wikipedia

wikipedia.set_lang("en")

load_dotenv()


class Utils(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.gis_api_key = os.getenv("GIS_API_KEY")
        self.gis_project_cx = os.getenv("GIS_PROJECT_CX")

        self.gis = GoogleImagesSearch(self.gis_api_key, self.gis_project_cx)


        self.custom_nsfw = [
            "gräfenberg spot",
            "shotacon",
            "shota",
            "male genitalia",
            "female genitalia",
            "cyclopia"
        ]

        self.imgs_path = "data/imgs/"

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

        if profanity.contains_profanity(query) or query.lower() in self.custom_nsfw:
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


    @commands.command(description="Posts an image for a given query.")
    async def image(self, ctx, *args):
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

        if profanity.contains_profanity(query) or query.lower() in self.custom_nsfw:
            if not ctx.channel.is_nsfw():
                await ctx.send("You can only search that in NSFW channels.")
                return

        search_params = {
            'q': query,
            'num': 1,
            'safe': 'medium',
            'fileType': 'jpg',
            'imgType': 'photo',
            'imgSize': 'imgSizeUndefined',
            'imgDominantColor': 'imgDominantColorUndefined',
            'rights': 'rightsUndefined'
        }

        filename = f'{query.replace(" ", "_")}'
        self.gis.search(search_params=search_params, path_to_dir=self.imgs_path, custom_image_name=filename)

        with open(f"{self.imgs_path}{filename}.jpg", "rb") as f:
            await ctx.send(file=discord.File(f))

        os.remove(f"{self.imgs_path}{filename}.jpg")


def setup(client):
    client.add_cog(Utils(client))
