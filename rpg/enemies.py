import random
import json
import copy

from rpg.entity import Entity
from utils.logger import Logger

customlogger = Logger("rpg/enemies.py")


class Pizza(Entity):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	TYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]
	STATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED", "SNARED", "POLYMORPHED"]

	def __init__(self, pizzatype):
		self.pizzatype = pizzatype.upper()
		self.validate()

		self.stats = copy.copy(self.STATS[self.pizzatype])
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])

		Entity.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])

		self.exp_gives = self.stats["exp"]


		self.attacks = {
			"NORMAL": [self.degeneracy_blade, self.waifu_smash, self.horny_aura, self.pizza_box, self.cheese_spread, self.greece_shot, self.roasted_to_perfection, self.master_of_comedy, self.flex, self.retardation, self.i_can_totally_do_this],
			"MADDENED": [self.waifu_smash, self.greece_shot, self.roasted_to_perfection, self.i_can_totally_do_this],
			"RELAXED": [self.pizza_box, self.cheese_spread, self.flex]
		}

		self.default_state = "NORMAL"
		self.state =  self.default_state

	def get_info(self):
		return f"**{self.pizzatype.title()} Pizza**\n{self.get_stat_info()}"

	def get_monster_info(self):
		return f"{self.pizzatype.title()} Pizza"

	def validate(self):
		if not (self.pizzatype in self.TYPES):
			raise Exception("Invalid pizza type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.STATES):
			raise Exception("Invalid pizza state.")

		self.state = new_state.upper()

	def get_random_attack(self):
		if self.state.upper() in ["STUNNED", "SNARED", "POLYMORPHED"]:
			state = self.state
			self.change_state("NORMAL")
			return f"**{self.get_monster_info()}** is currently **{state}** and cannot attack!"

		options = self.attacks[self.state]
		attack = random.choice(options)
		return attack

	async def death(self, ctx, players, effects):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")


	# ATTACKS

	async def degeneracy_blade(self, ctx, players, effects):
		# removes player(s) agility by making them fat
		pass

	async def waifu_smash(self, ctx, players, effects):
		# summons waifu who attacks the player dealing magic damage (magic only attack)
		pass

	async def horny_aura(self, ctx, players, effects):
		# stuns player(s) for 1 move cuz of horniness
		pass

	async def pizza_box(self, ctx, players, effects):
		# summons massive cardboard box to protect itself for the next 2 turns(ups physical defense)
		pass

	async def cheese_spread(self, ctx, players, effects):
		# spreads lots of cheese over himself (ups def and mr)
		pass

	async def greece_shot(self, ctx, players, effects):
		# throws greece balls at player(s) cuz pizza never showers, doing physical damage
		pass

	async def roasted_to_perfection(self, ctx, players, effects):
		# converts the room into an oven dealing more and more physical damage over 3 turns
		pass

	async def master_of_comedy(self, ctx, players, effects):
		# makes the player(s) cringe incredibly hard with his bad joke (lowers player defense (both physical and magical))
		pass

	async def flex(self, ctx, players, effects):
		# flexes his pen spinning techniques, sadly impressing nobody. (lowers own def and mr)
		pass

	async def retardation(self, ctx, players, effects):
		# makes the player(s) retarded. The player(s) use a random ability in their next turn.
		pass

	async def i_can_totally_do_this(self, ctx, players, effects):
		# charges towards the player(s) looking incredibly cool. Trips on a banana peel and loses half remaining hp.
		pass


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

		self.attacks = {
			"NORMAL": [],
			"MADDENED": [],
			"RELAXED": []
		}

		self.default_state = "NORMAL"
		self.state =  self.default_state

	def get_info(self):
		return f"**{self.nisttype.title()} Nist**\n{self.get_stat_info()}"

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

	async def death(self, ctx, players, effects):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")


	# ATTACKS

	async def snip_snip(self, ctx, players, effects):
		# nist cuts off a random percentage of the player(s) health (upto a limit)
		pass

	async def a_new_persona(self, ctx, players, effects):
		# nist changes his personality, confusing everybody and lowering their defenses (def and mr)
		pass

	async def did_i_just_catch_you_pirating(self, ctx, players, effects):
		# starts a rant against pirating, dealing a shit ton of mixed damage to all players (also increases agility)
		pass

	async def i_am_the_hentai_man(self, ctx, players, effects):
		# nist shows the players random hentai from the interwebs, distracting them. (decreses physcial and magic damage and agility of players)
		pass

	async def guys_see_my_edit_guys(self, ctx, players, effects):
		# shows the players his anime edits, embarassing himself cuz they turned out worse than the actual images. (loses half remaining hp)
		pass

	async def fucking_feminists(self, ctx, players, effects):
		# goes on a rant about how feminists are stupid and how he hates women. (gains shit ton of armor and mr) (if player is of class woman they take a huge percentage of their max health as damage.)
		pass

	async def editor_shield(self, ctx, players, effects):
		# edits a shield on his pc and uses it to defend himself (bonus armor for the next 2 turns)
		pass

	async def i_have_a_girlfriend_btw(self, ctx, players, effects):
		# starts talking about his girlfriend for absolutely no reason. Makes the players sleepy and miss a turn.
		pass

	async def idiot_complains_about_you(self, ctx, players, effects):
		# nist attemps to roast the players. 50% chance of dealing physcial damage to players.
		pass

	async def horrible_mic(self, ctx, players, effects):
		# nist joins the vc, making everyone's ears bleed cuz of his god aweful mic (deals mixed damage)
		pass
