import time
import discord
import asyncio
import json
import os

from discord.ext import commands
from utils.logger import Logger
from utils.id_generator import IdGenerator
from dotenv import load_dotenv

load_dotenv()


class TerminalGame(commands.Cog):
    def __init__(self, client):
        self.logger = Logger("cogs/terminalgame/TerminalGame")
        
        self.client = client
        self.output_file = os.getenv("TERMINAL_OUTPUT")
        self.input_file = os.getenv("TERMINAL_INPUT")
        self.registered = {}
        self.load_registered() 

    
    @commands.command(description="command")
    async def openterminal(self, ctx):
        if not str(ctx.author.id) in self.registered:
            await ctx.send("Please register first using !registeros.")
            return
        
        await ctx.send(f"Opened {ctx.author.name}'s terminal. (type exit whenever you want to quit)")
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author
        while True:
            self.logger.log_neutral("Waiting for command..")
            try:
                msg = await self.client.wait_for("message", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You didn't input a command for 1 minute. Exiting terminal.")
                return
            
            if msg.content.lower() == "exit":
                await ctx.send("Exiting terminal.")
                return

            self.logger.log_neutral("Got a command!")

            while True:
                time.sleep(1)
                try:
                    with open(self.input_file, "r+") as f:
                        inputs = json.load(f)
                        inputs.append({
                            "id": self.get_game_id(ctx.author),
                            "cmd": msg.content
                        })
                        f.truncate(0)
                        f.seek(0)
                        json.dump(inputs, f, indent=4)
                        self.logger.log_neutral("Added command to inputs!")
                        break
                except IOError:
                    continue

            while True:
                time.sleep(1)
                try:
                    with open(self.output_file, "r+") as f:
                        outputs = json.load(f)
                        response = outputs.pop(self.get_game_id(ctx.author))
                        f.truncate(0)
                        f.seek(0)
                        json.dump(outputs, f, indent=4)
                        break
                except IOError:
                    continue
                except KeyError:
                    self.logger.log_error("Key error")
                    continue
                
            self.logger.log_neutral("Got a response!")
            await ctx.send(f"```{response}```")
            
    
    @commands.command(description="register an os.")
    async def registeros(self, ctx):
        if str(ctx.author.id) in self.registered:
            await ctx.send("You are already registered for an OS.")
            return

        tempid = IdGenerator.generate_id()
        await ctx.send(f"{ctx.author.mention} DM me the password you want to choose for your system (or write it here, although i wouldn't recommend that). It cannot be more than 20 letters.")

        def check(msg):
            return (msg.channel == ctx.channel and msg.author == ctx.author and len(msg.content) < 21) or (isinstance(msg.channel, discord.channel.DMChannel) and msg.author == ctx.author and len(msg.content) < 21)

        
        try:
            msg = await self.client.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} You didn't reply with a password.")
            return

        while True:
            time.sleep(1)
            try:
                with open(self.input_file, "r+") as f:
                    inputs = json.load(f)
                    inputs.append({
                        "tempid":tempid,
                        "username": ctx.author.name,
                        "password": msg.content,
                    })
                    f.truncate(0)
                    f.seek(0)
                    json.dump(inputs, f, indent=4)
                    break
            except IOError:
                continue

        while True:
            time.sleep(1)
            try:
                with open(self.output_file, "r+") as f:
                    outputs = json.load(f)
                    newid = outputs[tempid]
                    self.register(str(ctx.author.id) , newid)
                    await ctx.send(f"Registered {ctx.author.mention}")
                    outputs.pop(tempid)
                    f.truncate(0)
                    f.seek(0)
                    json.dump(outputs, f, indent=4)
                    break
            except IOError:
                continue
            except KeyError:
                self.logger.log_error("Key error")
                continue

    def get_game_id(self, user):
        return self.registered[str(user.id)]
    
    def register(self, user_id, game_id):
        self.registered[user_id] = game_id
        self.save_registered()
    
    def save_registered(self):
        with open("data/registered_os.json", "w") as f:
            json.dump(self.registered, f, indent=4) 

    def load_registered(self):
        with open("data/registered_os.json", "r") as f:
            self.registered = json.load(f) 


def setup(client):
    client.add_cog(TerminalGame(client))