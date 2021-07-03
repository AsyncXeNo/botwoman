import discord
import random
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

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")

		await ctx.send("you moved to a new room!! (bro trust me)")
		self.client.get_cog("RPG").save_players()


	@commands.command(description="information about the room you are in the RPG.")
	async def roominfo(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")

		player = self.client.get_cog("RPG").get_player_by_id(ctx.author.id)
		if player:
			await ctx.send(f"**Info-**\n{player.room.get_info()}")


	@commands.command(description="Starts an event for the room that the player is currently in.")
	async def event(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")

		player = self.client.get_cog("RPG").get_player_by_id(ctx.author.id)
		if not player.room:
			await ctx.send("How tf are you not in a room? Please contact AsyncXeno#7777 and tell him how shit of a programmer he is thanks. As for the game, you can't play cuz you're SOMEHOW not inside the dungeon.")
		await player.room.start_event(ctx)


	# HELPER FUNCTIONS
	def validate(self):
		return self.client.get_cog("RPG").game


	@commands.command(description="TEST")
	@commands.is_owner()
	async def test(self, ctx):
		await ctx.send([friend.name for friend in self.client.get_cog("RPG").get_friends(ctx.author.id)])


def setup(client):
	client.add_cog(RPG_GAME(client))