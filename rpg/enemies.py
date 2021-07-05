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
	STATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED"]

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

	async def attack(self, ctx, players):
		if self.state.upper() == "STUNNED":
			await ctx.send(f"{self.get_monster_info()} is currently ***{self.state}*** and cannot attack!")
			return

		options = self.attacks[self.state]
		attack = random.choice(options)
		attack(ctx, players)
		await ctx.send(attack)

	async def death(self, ctx, players):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")


	# ATTACKS

	def degeneracy_blade(self, ctx, players):
		# removes player(s) agility by making them fat
		pass

	def waifu_smash(self, ctx, players):
		# summons waifu who attacks the player dealing magic damage (magic only attack)
		pass

	def horny_aura(self, ctx, players):
		# stuns player(s) for 1 move cuz of horniness
		pass

	def pizza_box(self, ctx, players):
		# summons massive cardboard box to protect itself for the next 2 turns(ups physical defense)
		pass

	def cheese_spread(self, ctx, players):
		# spreads lots of cheese over himself (ups def and mr)
		pass

	def greece_shot(self, ctx, players):
		# throws greece balls at player(s) cuz pizza never showers, doing physical damage
		pass

	def roasted_to_perfection(self, ctx, players):
		# converts the room into an oven dealing more and more physical damage over 3 turns
		pass

	def master_of_comedy(self, ctx, players):
		# makes the player(s) cringe incredibly hard with his bad joke (lowers player defense (both physical and magical))
		pass

	def flex(self, ctx, players):
		# flexes his pen spinning techniques, sadly impressing nobody. (lowers own def and mr)
		pass

	def retardation(self, ctx, players):
		# makes the player(s) retarded. The player(s) use a random ability in their next turn.
		pass

	def i_can_totally_do_this(self, ctx, players):
		# charges towards the player(s) looking incredibly cool. Trips on a banana peel and loses half remaining hp.
		pass


class Nist(Entity):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	TYPES = ["SMALL", "MEDIUM", "LARGE", "FEMI(NIST)"]
	STATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED"]
	
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

	async def attack(self, ctx, players):
		if self.state.upper() == "STUNNED":
			await ctx.send(f"{self.get_monster_info()} is currently ***{self.state}*** and cannot attack!")
			return

		options = self.attacks[self.state]
		attack = random.choice(options)
		attack(ctx, players)
		await ctx.send(attack)
	
	async def death(self, ctx, players):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")

		
	# ATTACKS

	def snip_snip(self, ctx, players):
		# nist cuts off a random percentage of the player(s) health (upto a limit)
		pass

	def a_new_persona(self, ctx, players):
		# nist changes his personality, confusing everybody and lowering their defenses (def and mr)	
		pass

	def did_i_just_catch_you_pirating(self, ctx, players):
		# starts a rant against pirating, dealing a shit ton of mixed damage to all players (also increases agility)
		pass

	def i_am_the_hentai_man(self, ctx, players):
		# nist shows the players random hentai from the interwebs, distracting them. (decreses physcial and magic damage and agility of players)
		pass

	def guys_see_my_edit_guys(self, ctx, players):
		# shows the players his anime edits, embarassing himself cuz they turned out worse than the actual images. (loses half remaining hp)
		pass

	def fucking_feminists(self, ctx, players):
		# goes on a rant about how feminists are stupid and how he hates women. (gains shit ton of armor and mr) (if player is of class woman they take a huge percentage of their max health as damage.)
		pass

	def editor_shield(self, ctx, players):
		# edits a shield on his pc and uses it to defend himself (bonus armor for the next 2 turns)
		pass

	def i_have_a_girlfriend_btw(self, ctx, players):
		# starts talking about his girlfriend for absolutely no reason. Makes the players sleepy and miss a turn.
		pass

	def idiot_complains_about_you(self, ctx, players):
		# nist attemps to roast the players. 50% chance of dealing physcial damage to players.
		pass

	def horrible_mic(self, ctx, players):
		# nist joins the vc, making everyone's ears bleed cuz of his god aweful mic (deals mixed damage)
		pass