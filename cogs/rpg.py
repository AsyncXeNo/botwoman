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

		self.game = False

		self.players = []
		self.friends = []

		self.classes = ["fighter", "mage", "assassin", "healer"]
		self.playerfilepath = "data/player_info.pickle"
		self.idsfilepath = "data/generated_ids.json"
		self.load_players()
		self.load_friends()


	# COMMANDS
		
	@commands.command(description="Start RPG")
	@commands.is_owner()
	async def start(self, ctx):
		room_range = range(len(self.players)) if len(self.players) >= 4 else 4
		await ctx.send("Setting up the dungeon...")
		self.dungeon = [[Room((col, row)) for row in range(room_range)] for col in range(room_range)]
		await ctx.send("Assigning players to random rooms...")
		for player in self.players:
			coords = Vector2()
			coords.x = self.dungeon.index(random.choice(self.dungeon))
			coords.y = self.dungeon[coords.x].index(random.choice(self.dungeon[coords.x]))
			self.dungeon[coords.x][coords.y].add_player(player)

		for row in self.dungeon:
			for room in row:
				await ctx.send(room.get_info())

		await ctx.send("All set!")
		self.game = True


	@commands.command(description="Stop the game (only meant to be used during development.)")
	@commands.is_owner()
	async def stop(self, ctx):
		self.game = False
		await ctx.send("Game has ended.")
	

	@commands.command(description="purges friends list and all registered players")
	@commands.is_owner()
	async def purge(self, ctx):
		self.friends = []
		self.players = []
		self.save_players()
		self.save_friends()

		await ctx.send("purged.")

	
	@commands.command(description="Show registered players")
	@commands.is_owner()
	async def showplayers(self, ctx):

		players = ""

		for player in self.players:
			user = self.client.get_user(player.user_id)
			if user:
				players += f"{user.name}#{user.discriminator}  [{user.id}]\n"
			else:
				await ctx.send(f"Cannot find user with id {player.user_id}")
		
		if players != "":
			await ctx.send(players)
		else:
			await ctx.send("No players regsitered.")

	
	@commands.command(description="Show list of friends")
	@commands.is_owner()
	async def showfriends(self, ctx):
		friends = ""
		for pair in self.friends:
			friends += f"{self.client.get_user(pair[0]).name}  <->  {self.client.get_user(pair[1]).name}\n"

		if friends == "":
			await ctx.send("No friends")
			return

		await ctx.send(friends)

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


	@commands.command(description="Send a friend request to another player.")
	async def friend(self, ctx, member: discord.Member):
		player_exists = False
		author_player = None
		player_to_add = None
		user_to_add = None
		user_id = member.id

		for player in self.players:
			user = self.client.get_user(player.user_id)
			if user.id == user_id:
				player_exists = True
				player_to_add = player
				user_to_add = user

			if user.id == ctx.author.id:
				author_player = player

		if not author_player:
			await ctx.send("Seems like you haven't even registered. You can't send friend request to another players if you aren't registered.")
			return

		if not player_exists:
			await ctx.send(f"{ctx.author.mention} the person you mentioned hasn't registered yet.")
			return

		for pair in self.friends:
			if (author_player.user_id == pair[0] and player_to_add.user_id == pair[1]) or (author_player.user_id == pair[1] and player_to_add.user_id == pair[0]):
				await ctx.send(f"You are already friends with {user_to_add.name}.")
				return

		if author_player.user_id == player_to_add.user_id:
			await ctx.send("You can't be friends with yourself dumbass")
			return

		def check(msg):
			return msg.channel == ctx.channel and msg.author == user_to_add

		msg = None
		
		for i in range(3):

			await ctx.send(f"{user_to_add.mention} {ctx.author.name} would like to be friends with you. Do you wanna accept? (Y/N)")

			msg = await self.client.wait_for("message", check=check)

			if not msg.content.lower() in ["y", "n"]:
				await ctx.send("That's not even an option...")
				if i == 2:
					await ctx.send("You're retarded I'm done with you.")
					return

			else:
				break

		for pair in self.friends:
			if (author_player.user_id == pair[0] and player_to_add.user_id == pair[1]) or (author_player.user_id == pair[1] and player_to_add.user_id == pair[0]):
				await ctx.send(f"You are already friends with {user_to_add.name}.")
				return

		if msg.content.lower() == "n":
			
			await ctx.send(f"{ctx.author.mention} {user_to_add.name} does not want to be friends with you. Cry.")

		elif msg.content.lower() == "y":
			await ctx.send(f"{ctx.author.mention} is now friends with {user_to_add.mention}!")
			self.save_friend_pair(author_player.user_id, player_to_add.user_id)
		

	@commands.command(description="Unfriend another player.")
	async def unfriend(self, ctx, member: discord.Member):
		self_id = ctx.author.id
		unfriend_id = member.id
		 
		friends = False

		for pair in self.friends:
			if (self_id == pair[0] and unfriend_id == pair[1]) or (self_id == pair[1] and unfriend_id == pair[0]):
				friends = True
				self.friends.pop(self.friends.index(pair))

		if not friends:
			await ctx.send("You are not friends with this user anyway.")
			return

		await ctx.send(f"{ctx.author.mention} lost all connections with {member.mention}.")


	# HELPER FUNCTIONS

	def save_friend_pair(self, friend1, friend2):
		self.friends.append((friend1, friend2,))
		self.save_friends()

	def save_friends(self):
		with open("data/friends.json", "w") as f:
			json.dump(self.friends, f, indent=4)

	def load_friends(self):
		with open("data/friends.json", "r") as f:
			self.friends = json.load(f)

	def save_player(self, user_id, character_class):
		self.players.append(Player(user_id, character_class, self.client.get_user(user_id).name))
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

class Player(object):
	def __init__(self, user_id, character_class, name):
		self.user_id = user_id
		self.character_class = character_class
		self.name = name

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}"


class Room(object):
	def __init__(self, pos):
		self.pos = pos
		self.players = []
		self.enemies = []
		self.events = []
		self.chests = []

	def add_player(self, player):
		self.players.append(player)

	def get_info(self):
		response = f"{self.pos}\n"
		for player in self.players:
			response += player.__str__()

		return response


class Vector2(object):
	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y

	def get_coords(self):
		return (x, y,)

	
def setup(client):
	client.add_cog(RPG(client))