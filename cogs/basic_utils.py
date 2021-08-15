import discord
import asyncio

from discord.ext import commands
from utils.my_logging import get_logger
from dotenv import load_dotenv


load_dotenv()
logger = get_logger(__name__)


class BasicUtils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="kick lol")
    @commands.is_owner()
    async def ban(self, ctx, member: discord.Member):
        await ctx.send(f"React to this message with :thumbsup: to vote for banning {member.name}. He will be banned once this message reaches 5 reactions")
        def check(reaction, user):
            return str(reaction.emoji) == '👍'
        reactions = 0 
        while not reactions == 5:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f"No reaction for the past 60 seconds. Guess {member.name} is not banned.")
                return
            
            reactions += 1
            await ctx.send(reactions)
        await member.kick()
        await ctx.send(f"Banned {member.name}")
        logger.info(f"Kicked {member.name}.")
                

    @commands.command(description='Unmutes the specified user.')
    @commands.is_owner()
    async def unmute(self, ctx, member: discord.Member):
        muterole = discord.utils.find(lambda g: g.name == 'Muted', ctx.guild.roles)
        await member.remove_roles(muterole)
        await ctx.send('Unmuted {0}.'.format(member.mention))
        logger.info('Unmuted {0}.'.format(member.name))


    @commands.command(description="Mutes the specified user.")
    @commands.is_owner()
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        muterole = discord.utils.find(lambda g: g.name == 'Muted', ctx.guild.roles)

        if not muterole:
            logger.warn('make a mute role dumbass\nExiting program...')
            return

        await ctx.send('{0} was muted.'.format(member.mention))
        await member.add_roles(muterole, reason=reason)
        logger.info('Muted {0}.'.format(member.name))


    @commands.command(description='Pings the bot.')
    async def ping(self, ctx):
        await ctx.send(f"{int(self.client.latency*1000)} ms")


    @commands.command(description="Gets your avatar.", aliases=["av"])
    async def avatar(self, ctx, member:discord.Member = None):
        if member:
            url = member.avatar_url
        else:
            url = ctx.author.avatar_url
        await ctx.send(url)


    @commands.command(description="you do not need to know")
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.client.load_extension(f'cogs.{extension}')
        await ctx.send("ok")
        logger.info(f"Loaded {extension}.")


    @commands.command(description="you do not need to know")
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        await ctx.send("ok")
        logger.info(f"Unloaded {extension}.")


    @commands.command(description="you do not need to know")
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.client.unload_extension(f'cogs.{extension}')
        self.client.load_extension(f'cogs.{extension}')
        logger.info(f"Reloaded {extension}.")
        await ctx.send("ok")


def setup(client):
    client.add_cog(BasicUtils(client))