import discord
from discord.ext import commands


class RPG_GAME(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.command(description="Moves you to another random room.")
	async def scout(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		await ctx.send("you moved to a new room!! (bro trust me)")


	# HELPER FUNCTIONS
	def validate(self):
		return self.client.get_cog("RPG").game


def setup(client):
	client.add_cog(RPG_GAME(client))