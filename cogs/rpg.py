import json
import pickle

# from rpg.players.player import Player
# from rpg.players.assassin import Assassin
# from rpg.players.mage import Mage
# from rpg.players.woman import Woman
# from rpg.players.fighter import Fighter
# from rpg.players.tank import Tank
# from rpg.parties.player_party import PlayerParty
from discord.ext import commands
# from utils.stats_parser import StatsParser
from utils.my_logging import get_logger


logger = get_logger(__name__)


class RPG(commands.Cog):
	def __init__(self, client):
		self.client = client
		
		self.registered = []
		self.parties = []

		# self.load_registered()

		# self.player_classes = {"ASSASSIN": Assassin, "WOMAN": Woman, "MAGE": Mage, "FIGHTER": Fighter, "TANK": Tank}
	

	# @commands.command(description="clear")
	# @commands.is_owner()
	# async def purge(self, ctx):
	# 	await ctx.send("Are you sure? [Y/n]")

	# 	def check(msg):
	# 		return msg.channel == ctx.channel and msg.author == ctx.author
	
	# 	msg = await self.client.wait_for("message", check=check)

	# 	if msg.content.upper() != "Y":
	# 		await ctx.send("Didn't proceed with purging.")
	# 		return

	# 	await ctx.send("**clearing all data.**")
	# 	self.clear()
	
	# @commands.command(description="This command will be used for all the tests.")
	# @commands.is_owner()
	# async def test(self, ctx):
	# 	await ctx.send("Creating a player and a party.")
	# 	with open("res/rpg/test_stats.json", "r") as f:
	# 		stats = json.load(f)
	# 	stats = StatsParser.parse_stats_range(stats["TEST"])
	# 	player = Player(ctx.author.name, str(ctx.author.id), stats["maxhp"], stats["str"], stats["mp"], stats["armor"], stats["mr"], stats["agility"], "Xeno Stacks", [])
	# 	party = PlayerParty(player)
	# 	await ctx.send(party.get_owner().get_name())


	# @commands.command(description="Shows a list of all registered players.")
	# async def showplayers(self, ctx):
	# 	msg = ""
	# 	for player in self.registered:
	# 		msg += f"`{player.get_name().upper()}\n{player.get_id()}`"

	# 	if msg == "":
	# 		await ctx.send("no players")
	# 		return

	# 	await ctx.send(msg)

	
	# @commands.command(description="Register for the RPG.")
	# async def register(self, ctx):
	# 	if self.is_registered(ctx.author.id):
	# 		logger.warn(f"{ctx.author.name} is already registered.")
	# 		await ctx.send(f"{ctx.author.name} is already registered.")
	# 		return
		
	# 	options = []
	# 	for player_class in self.player_classes:
	# 		options.append(player_class)

	# 	options_text = ""
	# 	for option in options:
	# 		options_text += f"```{option}```"

	# 	await ctx.send(f"Choose your class.\n{options_text}")

	# 	def check(msg):
	# 		return msg.channel == ctx.channel and msg.author == ctx.author

	# 	msg = await self.client.wait_for("message", check=check)

	# 	if not msg.content.upper() in options:
	# 		logger.warn(f"{ctx.author.name} is being retarded. Exiting command.")
	# 		await ctx.send("That is not an option (?)")
	# 		return

	# 	player = self.player_classes[msg.content.upper()](ctx.author.name, str(ctx.author.id))
	# 	self.register_player(player)


	# # helper
	# def clear(self):
	# 	logger.warn("This is going to clear all saved data once and for all. I hope you know what you're doing cuz this process is irreversible.")
	# 	self.registered = []
	# 	self.save_registered()

	# def register_player(self, player):
	# 	logger.warn(f"Player with name {player.get_name()} and id {player.get_id()} registered.")
	# 	self.registered.append(player)
	# 	self.save_registered()

	# def save_registered(self):
	# 	logger.info("Saving registered players in player_info.pickle.")
	# 	with open("data/player_info.pickle", "wb") as f:
	# 		pickle.dump(self.registered, f)

	# def load_registered(self):
	# 	logger.info("Loading registered players from player_info.pickle.")
	# 	with open("data/player_info.pickle", "rb") as f:
	# 		self.registered = pickle.load(f)

	# def is_registered(self, player_id:int):
	# 	for player in self.registered:
	# 		if player.get_id() == str(player_id):
	# 			return True
		
	# 	logger.warn(f"Didn't find any registered player with id {player_id}.")
	# 	return False

	# def get_player_by_id(self, player_id:int):
	# 	if not self.is_registered(player_id):
	# 		logger.warn(f"Didn't find any registered player with id {player_id}.")
	# 		return

	# 	for player in self.registered:
	# 		if player.get_id() == str(player_id):
	# 			return player
				

def setup(client):
	client.add_cog(RPG(client))
