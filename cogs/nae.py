import discord
import json
from discord import embeds
from discord.ext import commands


class Nae(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        with open('data/replies.json', 'r') as f:
            self.replies = json.load(f)
            
        with open('data/message_logs.json', 'r') as f:
            message_logs = json.load(f)

        message_data = {'author': message.author.name, 'message': message.content, 'channel': message.channel.name, 'atachments': [attachment.url for attachment in message.attachments], "embeds": [embed.url for embed in message.embeds], 'datetime': message.created_at.__str__()}

        message_logs.append(message_data) 

        with open('data/message_logs.json', 'w') as f:
            json.dump(message_logs, f, indent=4)
        
        if message.author == self.client.user:
            return
        
        for entry in self.replies:
            if self.replies[entry][1] == "NONE":
                if message.content.lower() == entry:
                    await message.channel.send(self.replies[entry][0])
            
            if self.replies[entry][1] == "START":
                if message.content.lower().endswith(entry):
                    await message.channel.send(self.replies[entry][0])


            if self.replies[entry][1] == "END":
                if message.content.lower().startswith(entry):
                    await message.channel.send(self.replies[entry][0])

            if self.replies[entry][1] == "MIDDLE":
                if entry in message.content.lower():
                    await message.channel.send(self.replies[entry][0])
    

def setup(client):
    client.add_cog(Nae(client))