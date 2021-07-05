import random
import copy
import json

from discord.utils import resolve_template

from rpg.entity import Entity
from rpg.room import Room
from rpg.attack import Attack
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
				Attack("Seduction", "Seduces everyone in the room. Increases physcial and magic damage for allies and decreases defense and magic resist for enemies.", self.seduction), 
				Attack("Shout for no reason", "Shouts for literally no reason, confusing the enemies, reducing their agility and lowering their hostility by 1. (MADDENED -> NORMAL or NORMAL -> RELAXED)", self.shout_for_no_reason), 
				Attack("DON'T TOUCH ME!", "Damage dealing abilities won't affect your party for the next turn.", self.dont_touch_me), 
				Attack("Slap!", "Slaps the enemies, dealing physcial damage which scales with player's stats.", self.slap), 
				Attack("cry for help...", "Starts crying loudly for help, causing the cops to arrive. They start beating the enemies dealing magic damage which scales with player's stats.", self.cry_for_help), 
				Attack("Pepper Spray", "Pepper sprays the enemies, blinding them and decresing their agility to 0 for 1 turn. Also does some mixed damage scaling with the player's stats.", self.pepper_spray), 
				Attack("(ULTIMATE) Women should be treated equally!!", "You steal your enemies' stats which last with you for the next 2 turns before reverting back to normal.", self.women_should_be_treated_equally)
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


	# ATTACKS

	# woman
	def seduction(self, ctx, enemies):
		# seduces everyone in the room. Increases str and magic for allies and decreases def and mr for enemies.
		pass

	def shout_for_no_reason(self, ctx, enemies):
		# shouts for literally no reason, confusing the enemies, reducing their agility and changing their state to "NORMAL"
		pass

	def dont_touch_me(self, ctx, enemies):
		# damage dealing abilities won't affect your party for the next turn.
		pass

	def slap(self, ctx, enemies):
		# slaps the enemies, dealing (str) physcial damage
		pass

	def cry_for_help(self, ctx, enemies):
		# starts crying loudly for help. Summons cops who beat up the enemies (does magic damage cuz i said so)
		pass

	def pepper_spray(self, ctx, enemies):
		# pepper sprays the enemies, blinding them. (decreses agility to 0 for 1 turn and does some mixed damage)
		pass
    
	def women_should_be_treated_equally(self, ctx, enemies):
		# ULTIMATE - steals her enemies' stats. They last with her for the next 2 turns before reverting back to normal.
		pass


	# fighter

	def mantis_style(self, ctx, enemies):
		# Northern Praying Mantis is a style of Chinese martial arts, sometimes called Shandong Praying Mantis after its province of origin. Increases armor and magic resist by a large amount.
		pass

	def monkey_style(self, ctx, enemies):
		# Monkey Kung Fu or Hóu Quán is a Chinese martial art which utilizes ape or monkey-like movements as part of its technique. Increases agility by a large amount.
		pass

	def viper_style(self, ctx, enemies):
		# The green bamboo viper is the snake style taught in the United States by Grandmaster Wing Loc Johnson Ng. Deals physcial damage as poison for the next 2 turns (including current turn).
		pass

	def tiger_style(self, ctx, enemies):
		# Deals physcial damage to the enemies, scaling with player's stats.
		pass

	def take_it_all(self, ctx, enemies):
		# Suppresses the feeling of pain, reducing the damage taken by 30%. Also restores 20 fury.
		pass

	def careless(self, ctx, enemies):
		# Sacrifices 10% of own hp to gain 40 fury.
		pass

	def dragon_style(self, ctx, enemies):
		# Takes 50% reduced damage for the next 2 turns. After that, unleases all the damage taken (increased based on fury) to the enemies as magic damage.
		pass


	# mage

	def polymorph(self, ctx, enemies):
		# Requires 50 energy stacks. Polymorphs a single enemy (if used against a party with multiple enemies, it chooses the enemy at random). They cannot do anything in their next turn and take increases damage from all sources.
		pass

	def demon_summon(self, ctx, enemies):
		# Summons demons directly from hell (1 demon per 10 energy stack) each doing magic damage which scales with the player's stats.
		pass

	def masic_missiles(self, ctx, enemies):	
		# Throws a bunch of magic missiles towards enemies, dealing magic damage which scales with the player's stats.
		pass

	def gods_grace(self, ctx, enemies):
		# Channels for the next turn, restoring 20 energy stacks gaining a magical shield for the duration which absorbs all kinds of damage. Amount of damage absorbed scales with the player's magic damage.
		pass

	def blizzard(self, ctx, enemies):
		# Stuns the enemies for 1 turn.
		pass

	def finger_of_death(self, ctx, enemies):
		# Requires 80 energy stacks. You send your enemies for judgement. There is a 50% chance they come out unharmed. If not, they take 40% max health magic damage and you restore 40 energy stacks
		pass

	def dark_vortex(self, ctx, enemies):
		# Sacrifice 95% of your remaining HP. Summons a whirling mass of dark energy, ripping through all resistances and doing crazy amounts of magical damage, scaling with energy stacks, the amount of hp sacrificed and player's stats (uses all energy stacks).
		pass


	# tanks
	
	def massacre(self, ctx, enemies):
		# Slams the enemies on the ground and pounds them, dealing physcial damage scaling with the player's stats.
		pass

	def rage(self, ctx, enemies):
		# Channels for 1 ability. Ups armor and magic resist and builds 20 resolve.
		pass

	def land_slide(self, ctx, enemies):
		# Causes a land slide, dealing some physcial damage to all enemies and reducing their agility. Also makes them prone to more damage by reducing their armor.
		pass

