import requests
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
        self.server_url = 'http://127.0.0.1:5555/commands'
        self.registered = {}
        self.load_registered() 

    
    @commands.command(description="command")
    async def openterminal(self, ctx):
        if not str(ctx.author.id) in list(self.registered.keys()):
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

            response = requests.post(url=self.server_url, data={
                'func': 'cmd',
                'info': json.dumps({
                    'id': self.get_game_id(ctx.author),
                    'input': msg.content
                })
            })

            if response.status_code != 200:
                self.logger.log_error(response.json())
                await ctx.send('something went wrong.')
                return
            
            response = response.json()
            if response['response_type'] == 'error':
                await ctx.send(response['response'])
                return
            elif response['response_type'] == 'success':
                response = response['response']
                
            self.logger.log_neutral("Got a response!")
        
            if isinstance(response, str):
                self.logger.log_error(response)
                await ctx.send('something went wrong.')
                return

            await ctx.send(f"```\nCommand exited with code {response['exit_code']}```")
            if response['stdout']:
                await ctx.send(f"```\n{response['stdout']}```")
            if response['stderr']:
                await ctx.send(f"```\n{response['stderr']}```")
            
            response = requests.post(url=self.server_url, data={
                'func': 'new_line',
                'info': json.dumps({
                    'id': self.get_game_id(ctx.author)
                })
            })

            if response.status_code != 200:
                self.logger.log_error(response.json())
                await ctx.send('something went wrong.')
                return
            
            response = response.json()
            if response['response_type'] == 'error':
                await ctx.send(response['response'])
                return
            elif response['response_type'] == 'success':
                await ctx.send(f'```{response["response"]}```')

            
    
    @commands.command(description="register an os.")
    async def registeros(self, ctx):
        if str(ctx.author.id) in list(self.registered.keys()):
            await ctx.send("You are already registered for an OS.")
            return

        await ctx.send(f"{ctx.author.mention} DM me the password that you want to choose for your system (or write it here, although i wouldn't recommend that). It cannot be more than 20 letters.")

        def check(msg):
            if isinstance(msg.channel, discord.channel.DMChannel) and msg.author == ctx.author and len(msg.content) < 21:
                return True
            return (msg.channel == ctx.channel and msg.author == ctx.author)
        
        try:
            msg = await self.client.wait_for("message", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} You didn't reply with a password.")
            return

        response = requests.post(url=self.server_url, data={
            'func': 'new',
            'info': json.dumps({
                'temp_id': ctx.author.id,
                'username': ctx.author.name,
                'password': msg.content
            })
        })

        if response.status_code != 200:
            self.logger.log_error(response.json())
            await ctx.send('something went wrong.')
            return
        
        response = response.json()
        if response['response_type'] == 'error':
            await ctx.send(response['response'])
            return
        elif response['response_type'] == 'success':
            self.register(str(ctx.author.id), response['response'])
            await ctx.send('Registered successfully.')
            return

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