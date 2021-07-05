import discord
import random
from discord.ext import commands

from rpg.enemies import Pizza, Nist
from utils.math import Vector2
from utils.logger import Logger

customlogger = Logger("cogs/rpg_game")


class RPG_GAME(commands.Cog):
	def __init__(self, client):
		self.client = client

		customlogger.log_neutral("Loaded rpg_game.")


	@commands.command(description="Shows the available attacks for your character")
	async def myattacks(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		if not self.validate_ctx(ctx):
			await ctx.send("Please use the command in the channel where the game is running.")
			return 

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")
			return

		player = self.client.get_cog("RPG").get_player_by_id(ctx.author.id)
		if player:
			await ctx.send(player.get_attack_info())

	@commands.command(description="information about the room you are in the RPG.")
	async def roominfo(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		if not self.validate_ctx(ctx):
			await ctx.send("Please use the command in the channel where the game is running.")
			return 

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")
			return

		player = self.client.get_cog("RPG").get_player_by_id(ctx.author.id)
		if player:
			await ctx.send(f"{player.room.get_info()}")


	@commands.command(description="Starts an event for the room that the player is currently in.")
	async def event(self, ctx):
		if not self.validate():
			await ctx.send("The game has not started yet.")
			return 

		if not self.validate_ctx(ctx):
			await ctx.send("Please use the command in the channel where the game is running.")
			return 

		if not self.client.get_cog("RPG").is_registered(ctx.author.id):
			await ctx.send("You are not even registered for the game. Please wait for current game to finish and then you can register using !register.")
			return

		if not self.client.get_cog("RPG").is_party_owner(ctx.author.id):
			await ctx.send("You do not own a party! Please tell your party owner (if you are in a party) to start the event.")
			return

		party = self.client.get_cog("RPG").get_party_by_owner_id(ctx.author.id)

		if not party[0].room:
			await ctx.send("How tf are you not in a room? Please contact AsyncXeno#7777 and tell him how shit of a programmer he is thanks. As for the game, you can't play cuz you're SOMEHOW not inside the dungeon.")

		await party[0].room.start_event(party[0])


	# HELPER FUNCTIONS
	def validate(self):
		return self.client.get_cog("RPG").game 

	def validate_ctx(self, ctx):
		return ctx.channel == self.client.get_cog("RPG").game_ctx.channel

	async def move_party(self, ctx, party):
		coords = Vector2()
		coords.y = self.client.get_cog("RPG").dungeon.index(random.choice(self.client.get_cog("RPG").dungeon))
		coords.x = self.client.get_cog("RPG").dungeon[coords.y].index(random.choice(self.client.get_cog("RPG").dungeon[coords.y]))

		
		self.client.get_cog("RPG").dungeon[coords.x][coords.y].add_party(party[0])

		await ctx.send("Moved to a new room.")


	@commands.command(description="TEST")
	@commands.is_owner()
	async def test(self, ctx):
		await self.client.get_cog("RPG").get_player_by_id(ctx.author.id).level_up(ctx)


def setup(client):
	client.add_cog(RPG_GAME(client))