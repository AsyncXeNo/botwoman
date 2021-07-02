import re
import json
import discord
from discord import message
from discord.ext import commands
from utils import Logger

customlogger = Logger("cogs/replies")


class Replies(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.regex_type = {
            0: "NONE",
            1: "START",
            2: "END",
            3: "MIDDLE"
        }

    
    @commands.command(description="Adds an automatic reply. (Regex implemented. No spaces before or after `%r`.) \nSyntax-> !addreply <sentence> | <reply>")
    async def addreply(self, ctx, *args):
        user_input = ' '.join(args)

        regex_pattern = re.compile('%r')

        sentence, reply = user_input.split('|')

        sentence, reply = sentence.strip().lower(), reply.strip()

        urls = re.findall(r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', reply)
        if len(urls) > 0:
            await ctx.send("No links buddy.")
            return

        customlogger.log_neutral(f"Adding reply: {sentence} -> {reply}")

        regex_type = self.regex_type[0]

        valid = False

        matches_iterator = re.finditer(regex_pattern, sentence)

        matches = []

        while True:
            try:
                match = next(matches_iterator)
                matches.append(match)
            except StopIteration:
                break

        if len(matches) > 2:
            await ctx.send("You cannot put 2 `%r`s. To know more about how this command works type !help addreply.")
            return

        elif len(matches) == 2:
            if not (matches[0].start() == 0 and matches[1].end() == len(sentence)):
                valid = False
                await ctx.send("Invalid syntax. Run !help addreply to know more about how this command works.")
                return
            valid = True
            sentence = sentence[2:-2]
            regex_type = self.regex_type[3]
            pass
        

        elif len(matches) == 1:
            if matches[0].start() == 0:
                valid = True
                sentence = sentence[2:]
                regex_type = self.regex_type[1]
            elif matches[0].end() == len(sentence):
                valid = True
                sentence = sentence[:-2]
                regex_type = self.regex_type[2]

        else:
            valid = True

        if not valid:
            return

        with open('data/replies.json', 'r') as f:
            replies = json.load(f)

        sentence = sentence.strip()
        replies[sentence] = (reply, regex_type)

        with open('data/replies.json', 'w') as f:
            json.dump(replies, f, indent=4)

        await ctx.send('Reply added.')


def setup(client):
    client.add_cog(Replies(client))