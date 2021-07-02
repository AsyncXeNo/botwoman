import discord
from discord.ext import commands

from rpg_entities import Pizza


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


	@commands.command(description="TEST")
	@commands.is_owner()
	async def test(self, ctx):
		pizza = Pizza("LARGE")
		await ctx.send(pizza.get_info())


def setup(client):
	client.add_cog(RPG_GAME(client))