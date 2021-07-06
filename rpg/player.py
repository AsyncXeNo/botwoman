import random
import copy
import json

from discord.utils import resolve_template

from rpg.entity import Entity
from rpg.room import Room
from rpg.attack import Attack
from rpg.attacks import *
from utils.logger import Logger

customlogger = Logger("rpg/player.py")


class Player(Entity):
	with open("res/rpg/playerstats.json", "r") as f:
		STATS = json.load(f)

	PLAYERCLASSES = ["MAGE", "FIGHTER", "WOMAN", "HEALER", "TANK"]
	PLAYERSTATES = ["NORMAL", "STUNNED"]
	def __init__(self, user_id, character_class, name):
		self.user_id = user_id
		self.character_class = self.PLAYERCLASSES[character_class]
		self.name = name

		self.stats = copy.copy(self.STATS[self.character_class])
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])

		Entity.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])

		self.exp_to_level_up = self.stats["exp"]

		self.level = 1
		self.exp = 0

		self.room = None

		self.attacks = {
			"MAGE": [],
			"FIGHTER": [],
			"WOMAN": [
				Attack("Seduction", "Seduces everyone in the room. Increases physcial and magic damage for allies and decreases defense and magic resist for enemies.", Woman.seduction),
				Attack("Shout for no reason", "Shouts for literally no reason, confusing the enemies, reducing their agility and lowering their hostility by 1. (MADDENED -> NORMAL or NORMAL -> RELAXED)", Woman.shout_for_no_reason),
				Attack("DON'T TOUCH ME!", "Damage dealing abilities won't affect you for the next turn.", Woman.dont_touch_me),
				Attack("Slap!", "Slaps the enemies, dealing physcial damage which scales with player's stats.", Woman.slap),
				Attack("cry for help...", "Starts crying loudly for help, causing the cops to arrive. They start beating the enemies dealing magic damage which scales with player's stats.", Woman.cry_for_help),
				Attack("Pepper Spray", "Pepper sprays the enemies, blinding them and decresing their agility to 0 for 1 turn. Also does some mixed damage scaling with the player's stats.", Woman.pepper_spray),
				Attack("(ULTIMATE) Women should be treated equally!!", "You steal your enemies' stats which last with you for the next 2 turns before reverting back to normal.", Woman.women_should_be_treated_equally)
			],
			"HEALER": [],
			"TANK": []
		}

		self.default_state = "NORMAL"
		self.state = self.default_state

		self.stacks = 0
		self.max_stacks = 100

	def get_attack_info(self):
		response = ""
		attacks = self.attacks[self.character_class]

		if self.level < 10:
			attacks = attacks[:-1]

		for attack in attacks:
			response += f"**__{attacks.index(attack) + 1}. {attack.name}__**\n*{attack.description}*\n\n"

		if response == "":
			response = "How tf did this happen. Please contact AsyncXeno#7777 and tell him how fucking stupid he is."
			raise Exception("No attacks (somehow)")
		return response

	def change_state(self, new_state):
		if not (new_state.upper() in self.PLAYERSTATES):
			raise Exception("Invalid player state.")

		self.state = new_state.upper()

	def set_room(self, room):
		if type(room) != Room:
			raise Exception("Invalid room")

		self.room = room

	async def level_up(self, ctx):
		old_level = self.level

		if self.level != 10:
			self.level += 1
			old_max_hp = self.maxhp
			self.maxhp = self.maxhp + int(self.maxhp * 1/2)
			old_physical = self.physical
			if self.physical != None:
				self.physical = self.physical + int(self.physical * 1/2)
			old_magic = self.magic
			if self.magic != None:
				self.magic = self.magic + int(self.magic * 1/2)
			old_def = self.defense
			self.defense = self.defense + int(self.defense * 1/2)
			old_magic_def = self.magic_def
			self.magic_def = self.magic_def + int(self.magic_def * 1/2)
			self.exp_to_level_up = self.exp_to_level_up + int(self.exp_to_level_up * 1/2)
			await ctx.send(f"**{self.name}** just leveled up! (*{old_level}* -> *{self.level}*)\n```MAX HP - {old_max_hp} -> {self.maxhp}\nPHYSCIAL DAMAGE - {old_physical} -> {self.physical}\nMAGICAL DAMAGE - {old_magic} -> {self.magic}\nPHYSCIAL DEFENSE - {old_def} -> {self.defense}\nMAGICAL DEFENSE - {old_magic_def} -> {self.magic_def}```")

		else:
			await ctx.send(f"**{self.name}** is already max level! (*{self.level}*)")


	async def attack(self, ctx, enemies):
		if self.state.upper() == "STUNNED":
			await ctx.send(f"**{self.name}** is currently ***{self.state}*** and cannot attack!")


	async def give_exp(self, ctx, exp):
		self.exp += exp
		self.check_if_level_up(ctx)
		await ctx.send(f"**{self.name}** you just gained {exp} experience points!")

	def check_if_level_up(self, ctx):
		if self.exp > self.exp_to_level_up:
			self.exp = self.exp - self.exp_to_level_up
			self.level_up(ctx)
			self.check_if_level_up(ctx)

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}\n"

	def get_info(self):
		return f"{self.__str__()}\n{self.get_stat_info()}"
