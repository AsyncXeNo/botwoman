import discord
import json
import random
import string
import pickle
from discord.ext import commands
from discord.utils import get


class RPG(commands.Cog):
	def __init__(self, client):
		self.client = client

		self.players = []
		self.friends = Friends()

		self.classes = ["fighter", "mage", "assassin", "healer"]
		self.playerfilepath = "data/player_info.pickle"
		self.idsfilepath = "data/generated_ids.json"
		self.load_players()


	# COMMANDS
		
	@commands.command(description="Start RPG")
	@commands.is_owner()
	async def start(self, ctx):
		self.dungeon = [[[] for _ in len(self.players)] for _ in len(self.players)]

	
	@commands.command(description="Show registered players")
	@commands.is_owner()
	async def show_players(self, ctx):

		players = ""

		for player in self.players:
			user = self.client.get_user(player.user_id)
			if user:
				players += f"{user.name}#{user.discriminator}\n"
			else:
				await ctx.send(f"Cannot find user with id {player.user_id}")
		
		if players != "":
			await ctx.send(players)
		else:
			await ctx.send("No players regsitered.")


	@commands.command(description="Register yourself in the RPG.")
	async def register(self, ctx):
		user_id = ctx.author.id

		for player in self.players:
			if player.user_id == user_id:
				await ctx.send("You are already registered.")
				return

		await ctx.send("Choose your class. (Mage / Fighter / Assassin / Healer)")

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel

		msg = await self.client.wait_for("message", check=check)

		if not (msg.content.lower() in self.classes):
			await ctx.send("What are you pizza? That was not even an option wtf?")
			return

		else:
			character_class = self.classes.index(msg.content.lower())

		self.save_player(user_id, character_class)

		await ctx.send("Registered successfully.")


	@commands.command(description="Change your class")
	async def changeclass(self, ctx):
		user_id = ctx.author.id

		registered = False

		for player in self.players:
			if player.user_id == user_id:
				registered = True

		if not registered:
			await ctx.send("Register first using !register.")
			return
		
		await ctx.send("Change your class. (Mage / Fighter / Assassin / Healer)")

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel

		msg = await self.client.wait_for("message", check=check)

		if not (msg.content.lower() in self.classes):
			await ctx.send("What are you pizza? That was not even an option wtf?")
			return

		else:
			new_class = self.classes.index(msg.content.lower())

		for player in self.players:
			if player.user_id == user_id:
				player.character_class = new_class

		self.save_players()

		await ctx.send("Class changed successfully.")


	
	

	# HELPER FUNCTIONS

	def save_player(self, user_id, character_class):
		self.players.append(Player(user_id, character_class))
		self.save_players()


	def save_players(self):
		with open(self.playerfilepath, "wb") as f:
			pickle.dump(self.players, f)


	def load_players(self):
		with open(self.playerfilepath, "rb") as f:
			self.players = pickle.loads(f.read()) 

	
	def generate_id(self):
		length  = 8

		with open(self.idsfilepath, "r") as f:
			generated = json.load(f)
			
		gen = ''.join(random.choices(string.ascii_uppercase, k=length))

		while gen in generated:
			gen = ''.join(random.choices(string.ascii_uppercase, k=length))

		generated.append(gen)

		with open(self.idsfilepath, "w") as f:
			json.dump(generated, f, indent=4)

		return gen
		

class Friends(object):
	def __init__(self):
		self.friends = [] # tuples of Player objects

	def add_friends(self, player1, player2):
		self.friends.append((player1, player2,))

	def get_friends(self):
		return self.friends


class Player(object):
	def __init__(self, user_id, character_class):
		self.user_id = user_id
		self.character_class = character_class

	def __str__(self):
		return f"Id- {self.user_id}\nClass- {self.character_class}"

	
def setup(client):
	client.add_cog(RPG(client))