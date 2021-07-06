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
			"MAGE": [
				Attack("Polymorph", "Requires 40 energy stacks. Polymorphs the enemies for 1 turn. They cannot do anything in their next turn and take increases damage from all sources.", Mage.polymorph),
				Attack("Demon summon!", "Summons demons directly from hell (1 demon per 10 energy stack) each doing magic damage which scales with the player's stats.", Mage.demon_summon),
				Attack("Magic missiles", "Throws a bunch of magic missiles towards enemies, dealing magic damage which scales with the player's stats. (doesn't use stacks)", Mage.magic_missiles),
				Attack("God's grace", "Channels for the next turn, restoring 20 energy stacks gaining a magical shield for the duration which absorbs all kinds of damage. Amount of damage absorbed scales with the player's magic damage.", Mage.gods_grace),
				Attack("Blizzard", "Requires 30 stacks. Stuns the enemies for 1 turn.", Mage.blizzard),
				Attack("Judgement", "Requires 80 energy stacks. You send your enemies for judgement. There is a 50% chance they come out unharmed. If not, they take 40% max health magic damage and you restore 40 energy stacks", Mage.judgement),
				Attack("Dark Vortex", "Sacrifice 95% of your remaining HP. Summons a whirling mass of dark energy, ripping through all resistances and doing crazy amounts of magical damage, scaling with energy stacks, the amount of hp sacrificed and player's stats (uses all energy stacks).", Mage.dark_vortex)
			],
			"FIGHTER": [
				Attack("Mantis Style", "Northern Praying Mantis is a style of Chinese martial arts, sometimes called Shandong Praying Mantis after its province of origin. Increases armor and magic resist by a large amount.", Fighter.mantis_style),
				Attack("Monkey Style", "Monkey Kung Fu or Hóu Quán is a Chinese martial art which utilizes ape or monkey-like movements as part of its technique. Increases agility by a large amount.", Fighter.monkey_style),
				Attack("Viper Style", "The green bamboo viper is the snake style taught in the United States by Grandmaster Wing Loc Johnson Ng. Deals physcial damage as poison for the next 2 turns (including current turn).", Fighter.viper_style),
				Attack("Tiger Style", "Deals physcial damage to the enemies, scaling with player's stats.", Fighter.tiger_style),
				Attack("Take it all!", "Suppresses the feeling of pain, reducing the damage taken by 40%. Also restores 20 fury.", Fighter.take_it_all),
				Attack("Furiosity", "Sacrifices 20% of own maxhp to gain 40 fury.", Fighter.furiosity),
				Attack("Dragon Style!", "Takes 60% reduced damage for the next 2 turns. After that, unleases all the damage taken (increased based on fury) to the enemies as magic damage.", Fighter.dragon_style)
			],
			"WOMAN": [
				Attack("Seduction", "Seduces everyone in the room. Increases physcial and magic damage for allies and decreases defense and magic resist for enemies.", Woman.seduction),
				Attack("Shout for no reason", "Shouts for literally no reason, confusing the enemies, reducing their agility and lowering their hostility by 1. (MADDENED -> NORMAL or NORMAL -> RELAXED)", Woman.shout_for_no_reason),
				Attack("DON'T TOUCH ME!", "Damage dealing abilities won't affect you for the next turn.", Woman.dont_touch_me),
				Attack("Slap!", "Slaps the enemies, dealing physcial damage which scales with player's stats.", Woman.slap),
				Attack("cry for help...", "Starts crying loudly for help, causing the cops to arrive. They start beating the enemies dealing magic damage which scales with player's stats.", Woman.cry_for_help),
				Attack("Pepper Spray", "Pepper sprays the enemies, blinding them and decresing their agility to 0 for 1 turn. Also does some mixed damage scaling with the player's stats.", Woman.pepper_spray),
				Attack("(ULTIMATE) Women should be treated equally!!", "You steal your enemies' stats which last with you for the next 2 turns before reverting back to normal.", Woman.women_should_be_treated_equally)
			],
			"HEALER": [
				Attack("SOON", "IN DEVELOPMENT", None)
			],
			"TANK": [
				Attack("Massacre", "Slams the enemies on the ground and pounds them, dealing physcial damage scaling with the player's stats.", Tank.massacre),
				Attack("Rage", "Channels for 1 ability. Ups armor and magic resist and builds 20 resolve.", Tank.rage),
				Attack("Land slide", "Causes a land slide, reducing their agility. Also makes them prone to more damage by reducing their armor.", Tank.land_slide),
				Attack("Taunt", "Requires 30 resolve. Taunts the enemies, making them focus the player. Enemy abilities in the next turn only affect you but they do twice the damage.", Tank.taunt),
				Attack("Intimidate", "Requires 20 resolve. Intimidates the enemies, fearing them. 20% chance of stunning the enemies for 1 turn and lowers their damage permanently. If enemies are stunned, restores 40 resolve", Tank.intimidate),
				Attack("Confrontation!", "Temporarily disable your resistances and take all your opponent's damage head on. In the next turn, do 140% of the damage taken as physcial damage. (requires 50 stacks)", Tank.confrontation),
				Attack("Warcry", "uses 100 resolve stacks. Starts an inspirational speech, motivating everybody in the party and giving them attack buffs, while gaining a lot of armor and mr himself. The power of the speech and buffs scale with the player's % missing health.", Tank.war_cry)
			]
		}

		self.default_state = "NORMAL"
		self.state = self.default_state

		self.stacks = 0
		self.max_stacks = 100

	def get_attack_info(self):
		response = ""
		attacks = self.attacks[self.character_class]

		if self.level < 10 and len(attacks) == 7:
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
