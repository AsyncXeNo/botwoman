import discord
import json
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

        message_logs.append({'author': message.author.name, 'message': message.content, 'channel': message.channel.name, 'atachments': [attachment.url for attachment in message.attachments], 'datetime': message.created_at.__str__()}) 

        with open('data/message_logs.json', 'w') as f:
            json.dump(message_logs, f, indent=4)
        
        if message.author == self.client:
            return
        
        for entry in self.replies:
            if message.content.lower() == entry:
                await message.channel.send(self.replies[entry])

    

def setup(client):
    client.add_cog(Nae(client))