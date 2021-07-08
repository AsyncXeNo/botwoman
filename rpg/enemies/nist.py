import random
import json
import copy

from rpg.entity import Entity
from rpg.attack import Attack
from utils.logger import Logger

customlogger = Logger("rpg/enemies/nist.py")


class Nist(Entity):
	with open("res/rpg/niststats.json", "r") as f:
		STATS = json.load(f)

	TYPES = ["SMALL", "MEDIUM", "LARGE", "FEMI(NIST)"]
	STATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED", "SNARED", "POLYMORPHED"]

	def __init__(self, nisttype):
		self.nisttype = nisttype.upper()
		self.validate()

		self.stats = copy.copy(self.STATS[self.nisttype])
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])

		Entity.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])

		self.exp_gives = self.stats["exp"]

		self.personalities = ["NORMAL", "SIMP", "INCEL"]
		self.default_personality = "NORMAL"
		self.personality = self.default_personality

		self.attacks = {
			"NORMAL": [
				Attack("Snip Snip", "Nist cuts off a random percentage of the players' health, (up to a limit)", self.snip_snip),
				Attack("A New Persona", "Nist changes his personality, confusing everybody and lowering their defenses.", self.snip_snip),
				Attack("Did I just catch you pirating???", "", self.did_i_just_catch_you_pirating),
				Attack("I am the Hentai man.", "", self.i_am_the_hentai_man),
				Attack("I have a girlfriend btw", "", self.i_have_a_girlfriend_btw),
				Attack("Guys see my edit guys", "", self.guys_see_my_edit_guys),
				Attack("Fucking feminists", "", self.fucking_feminists),
				Attack("Editor shield", "", self.editor_shield),
				Attack("Idiot complains about you", "", self.idiot_complains_about_you),
				Attack("Horrible mic", "", self.horrible_mic)
			],
			"MADDENED": [
				Attack("Snip Snip", "Nist cuts off a random percentage of the players' health, (up to a limit)", self.snip_snip),
				Attack("Did I just catch you pirating???", "", self.did_i_just_catch_you_pirating),
				Attack("Idiot complains about you", "", self.idiot_complains_about_you),
				Attack("Horrible mic", "", self.horrible_mic)
			],
			"RELAXED": [

			]
		}

		self.default_state = "NORMAL"
		self.state =  self.default_state

	def get_info(self):
		return f"{self.get_other_info()}\n{self.get_stat_info()}"

	def get_other_info(self):
		return f"State - {self.state}\nPersonality - {self.personality}"

	def get_monster_info(self):
		return f"{self.nisttype.title()} Nist"

	def validate(self):
		if not (self.nisttype in self.TYPES):
			raise Exception("Invalid nist type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.STATES):
			raise Exception("Invalid nist state.")

		self.state = new_state.upper()

	def get_random_attack(self):
		if self.state.upper() in ["STUNNED", "SNARED", "POLYMORPHED"]:
			state = self.state
			self.change_state("NORMAL")
			return f"**{self.get_monster_info()}** is currently **{state}** and cannot attack!"

		options = self.attacks[self.state]
		attack = random.choice(options)
		return attack

	async def death(self, ctx, players):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")


	# ATTACKS

	async def snip_snip(self, enemy, ctx, players, enemies, effects, client):
		# nist cuts off a random percentage of the player(s) health (upto a limit)
		await ctx.send("snip snip")

	async def a_new_persona(self, enemy, ctx, players, enemies, effects, client):
		# nist changes his personality, confusing everybody and lowering their defenses (def and mr)
		pass

	async def did_i_just_catch_you_pirating(self, enemy, ctx, players, enemies, effects, client):
		# starts a rant against pirating, dealing a shit ton of mixed damage to all players (also increases agility)
		pass

	async def i_am_the_hentai_man(self, enemy, ctx, players, enemies, effects, client):
		# nist shows the players random hentai from the interwebs, distracting them. (decreses physcial and magic damage and agility of players)
		pass

	async def guys_see_my_edit_guys(self, enemy, ctx, players, enemies, effects, client):
		# shows the players his anime edits, embarassing himself cuz they turned out worse than the actual images. (loses half remaining hp)
		pass

	async def fucking_feminists(self, enemy, ctx, players, enemies, effects, client):
		# goes on a rant about how feminists are stupid and how he hates women. (gains shit ton of armor and mr) (if player is of class woman they take a huge percentage of their max health as damage.)
		pass

	async def editor_shield(self, enemy, ctx, players, enemies, effects, client):
		# edits a shield on his pc and uses it to defend himself (bonus armor for the next 2 turns)
		pass

	async def i_have_a_girlfriend_btw(self, enemy, ctx, players, enemies, effects, client):
		# starts talking about his girlfriend for absolutely no reason. Makes the players sleepy and miss a turn.
		pass

	async def idiot_complains_about_you(self, enemy, ctx, players, enemies, effects, client):
		# nist attemps to roast the players. 50% chance of dealing physcial damage to players.
		pass

	async def horrible_mic(self, enemy, ctx, players, enemies, effects, client):
		# nist joins the vc, making everyone's ears bleed cuz of his god aweful mic (deals mixed damage)
		pass
