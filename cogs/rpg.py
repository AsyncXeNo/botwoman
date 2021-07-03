import discord
import json
import random
import string
import pickle
from discord.ext import commands
from discord.utils import get

from rpg_entities import *


class RPG(commands.Cog):
	def __init__(self, client):
		self.client = client

		self.game = False

		self.players = []
		self.parties = []

		self.game_ctx = None

		self.playerfilepath = "data/player_info.pickle"
		self.idsfilepath = "data/generated_ids.json"

		self.load_players()
		self.load_friends()


	# COMMANDS
		
	@commands.command(description="Start RPG")
	@commands.is_owner()
	async def start(self, ctx):

		if self.game:
			await ctx.send("A game is already in progress!")
			return

		room_range = range(len(self.players)) if len(self.players) >= 4 else 4
		await ctx.send("Setting up the dungeon...")
		self.dungeon = [[Room((col, row), ctx, self.client) for row in range(room_range)] for col in range(room_range)]
		await ctx.send("Assigning parties to random rooms...")

		for party in self.parties:
			coords = Vector2()
			coords.y = self.dungeon.index(random.choice(self.dungeon))
			coords.x = self.dungeon[coords.y].index(random.choice(self.dungeon[coords.y]))

			self.dungeon[coords.x][coords.y].add_party(party[0])

		for row in self.dungeon:
			for room in row:
				await ctx.send(room.get_info())


		await ctx.send("All set!")
		self.game = True
		self.game_ctx = ctx


	@commands.command(description="Stop the game (only meant to be used during development.)")
	@commands.is_owner()
	async def stop(self, ctx):
		if not self.game:
			await ctx.send("No game in progress anyway...")
			return 

		self.game = False
		await ctx.send("Game has ended.")
	

	@commands.command(description="purges friends list and all registered players")
	@commands.is_owner()
	async def purge(self, ctx):
		self.parties = []
		self.players = []
		self.save_players()

		await ctx.send("purged.")


	@commands.command(description="removes all records of AsyncXeno#7777")
	@commands.is_owner()
	async def purgeme(self, ctx):
		self.players.remove(self.get_player_by_id(ctx.author.id))
		self.save_players()
		await ctx.send("ok")

	
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

	@commands.command(description="Shows parties")
	@commands.is_owner()
	async def showparties(self, ctx):
		response = ""
		parties = [[friend.name for friend in party] for party in self.parties]
		for party in parties:
			response += f"PARTY -> {party}\n"

		if response == "":
			await ctx.send("No parties.")
			return

		await ctx.send(response)


	@commands.command(description="Shows info about a player.")
	async def info(self, ctx):
		if not self.is_registered(ctx.author.id):
			await ctx.send("You need to register first...")
			return

		response = "**Info-**\n"
		response += self.get_player_by_id(ctx.author.id).get_info()
		await ctx.send(response)


	@commands.command(description="Shows a user's friends.")
	async def myfriends(self, ctx):

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register in order to make friends.")
			return

		friends = ""
		for pair in self.friends:
			if pair[0] == ctx.author.id:
				friends += f"{self.client.get_user(pair[1]).name}\n"
			if pair[1] == ctx.author.id:
				friends += f"{self.client.get_user(pair[0]).name}\n"

		if friends != "":
			await ctx.send(friends)

		else:
			await ctx.send("You have no friends. Just like real life.")


	@commands.command(description="Make a party")
	async def makeparty(self, ctx):
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register in order to make a party.")
			return

		if self.party(ctx.author.id):
			await ctx.send("Seems like you are already in a party. Exit the party to make a new one.")
			return

		self.parties.append([self.get_player_by_id(ctx.author.id)])

		await ctx.send(f"Successfully created {self.get_player_by_id(ctx.author.id).name}'s party!")


	@commands.command(description="Join someone's party")
	async def joinparty(self, ctx, member:discord.Member):

		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register.")
			return

		party_owner = self.get_player_by_id(member.id)
		is_owner = False
		party_index = None

		for party in self.parties:
			if party[0].user_id == party_owner.user_id:
				is_owner = True
				party_index = self.parties.index(party)

		if self.party(ctx.author.id):
			await ctx.send("Seems like you are already in a party. Exit the party to make a new one.")
			return

		if not is_owner:
			await ctx.send("The person you mentioned doesn't own any party")
			return

		if is_owner and party_index != None:
			self.parties[party_index].append(self.get_player_by_id(ctx.author.id))
			await ctx.send(f"Successfully joined {self.get_player_by_id(self.parties[party_index][0].user_id)}'s party!")


	@commands.command(description="Leave whichever party you are a part of.")
	async def leaveparty(self, ctx):
		
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register.")
			return

		if not self.party(ctx.author.id):
			await ctx.send("You are currently not in any party.")
			return

		for party in self.parties:
			for friend in party:
				if friend.user_id == ctx.author.user_id:
					party_index = self.parties.index(party)
					player = friend

		if self.parties[party_index].index(player) == 0:
			await ctx.send("Are you sure you want to dismantle your party? (Y/N)")

			def check(msg):
				return msg.author == ctx.author and msg.channel == ctx.channel

			count = 0
			while True:
				msg = await self.client.wait_for("message", check=check)

				if not msg.content.lower() in ["y", "n"]:
					await ctx.send("That's not even an option wtf?")

				elif msg.content.lower() == "y":
					self.parties.remove(self.parties[party_index])

				elif msg.content.lower() == "n":
					await ctx.send("Alright then.")
					return

				count += 1
				if count == 3:
					await ctx.send("You are retarded I'm done with you.")
					return

		else:
			self.parties[party_index].remove(player)
			await ctx.send(f"You are no longer in a {self.parties[party_index][0].name}'s party.")
			return


	@commands.command(description="See your party.")
	async def myparty(self, ctx):
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register.")
			return

		if not self.party(ctx.author.id):
			await ctx.send("You are currently not in any parties.")

		for party in self.parties:
			for friend in party:
				if friend.user_id == ctx.author.id:
					await ctx.send(f"**{self.parties[self.parties.index(party)][0].name}'s Party:**\n```{', '.join([self.parties[self.parties.index(party)]])}```")


	@commands.command(description="Register yourself in the RPG.")
	async def register(self, ctx):

		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		user_id = ctx.author.id

		for player in self.players:
			if player.user_id == user_id:
				await ctx.send("You are already registered.")
				return

		options = [option.title() for option in Player.PLAYERCLASSES]
		options_str = " / ".join(options)
		await ctx.send(f"Choose your class. ({options_str})")

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel

		msg = await self.client.wait_for("message", check=check)

		if not (msg.content.upper() in Player.PLAYERCLASSES):
			await ctx.send("What are you pizza? That was not even an option wtf?")
			return

		else:
			character_class = Player.PLAYERCLASSES.index(msg.content.upper())

		self.save_player(user_id, character_class)

		await ctx.send("Registered successfully.")


	@commands.command(description="Change your class")
	async def changeclass(self, ctx):
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register.")
			return

		user_id = ctx.author.id

		registered = False

		for player in self.players:
			if player.user_id == user_id:
				registered = True

		if not registered:
			await ctx.send("Register first using !register.")
			return
		
		options = [option.title() for option in Player.PLAYERCLASSES]
		options_str = " / ".join(options)
		await ctx.send("Change your class. (Mage / Fighter / Assassin / Healer)")

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel

		msg = await self.client.wait_for("message", check=check)

		if not (msg.content.upper() in Player.PLAYERCLASSES):
			await ctx.send("What are you pizza? That was not even an option wtf?")
			return

		else:
			new_class = Player.PLAYERCLASSES.index(msg.content.upper())

		for player in self.players:
			if player.user_id == user_id:
				player.character_class = new_class

		self.save_players()

		await ctx.send("Class changed successfully.")


	@commands.command(description="Send a friend request to another player.")
	async def friend(self, ctx, member: discord.Member):
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register in order to make friends.")
			return

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
		if self.game:
			await ctx.send("A game is currently in progress!")
			return

		if not self.is_registered(ctx.author.id):
			await ctx.send("You are not registered for the RPG. Please register using !register in order to make friends.")
			return
			
		self_id = ctx.author.id
		unfriend_id = member.id
		 
		friends = False

		await ctx.send(f"Are you sure you don't wanna be friends with {self.get_player_by_id(unfriend_id).name} anymore? (Y/N)")

		def check(msg):
			return msg.author == ctx.author and msg.channel == ctx.channel

		count = 0

		while True:
			msg = await self.client.wait_for("message", check=check)
			if msg.content.lower() == "y":
				break
			elif msg.content.lower() == "n":
				await ctx.send("Then why waste my time???")
				return

			else:
				await ctx.send("That is not even an option wtf?")
				count += 1

				if count == 3:
					await ctx.send("You are retarded I'm done with you.")
					return

		for pair in self.friends:
			if (self_id == pair[0] and unfriend_id == pair[1]) or (self_id == pair[1] and unfriend_id == pair[0]):
				friends = True
				self.friends.pop(self.friends.index(pair))

		if not friends:
			await ctx.send("You are not friends with this user anyway.")
			return

		self.save_friends()
		await ctx.send(f"{ctx.author.mention} lost all connections with {member.mention}.")


	# HELPER FUNCTIONS

	def get_party_by_owner_id(self, owner_id):
		for party in self.parties:
			if party[0].user_id == owner_id:
				return party

		return None

	def is_party_owner(self, user_id):
		for party in self.parties:
			if party[0].user_id == user_id:
				return True

		return False

	def party(self, user_id):
		for party in self.parties:
			for player in party:
				if player.user_id == user_id:
					return True

		return False

	def get_friends(self, user_id):
		friends = []
		for pair in self.friends:
			if pair[0] == user_id:
				friends.append(pair[1])
			elif pair[1] == user_id:
				friends.append(pair[0])

		friends = [self.get_player_by_id(friend) for friend in friends]
		return friends

	def are_friends(self, player1_user_id, player2_user_id):
		for pair in self.friends:
			if pair[0] == player1_user_id:
				if pair[1] == player2_user_id:
					return True

			elif pair[1] == player1_user_id:
				if pair[0] == player2_user_id:
					return True

		return False

	def is_registered(self, user_id):
		registered = False

		for player in self.players:
			if player.user_id == user_id:
				registered = True

		return registered

	def get_player_by_id(self, user_id):
		for player in self.players:
			if player.user_id == user_id:
				return player

		return None

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


class Vector2(object):
	def __init__(self, x=None, y=None):
		self.x = x
		self.y = y

	def get_coords(self):
		return (x, y,)

	
def setup(client):
	client.add_cog(RPG(client))