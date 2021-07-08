import random
import json
import copy

from rpg.entity import Entity
from rpg.attack import Attack
from utils.logger import Logger

customlogger = Logger("rpg/enemies/pizza.py")


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
			"NORMAL": [ 
				Attack("Waifu Smash", "", self.waifu_smash), 
				Attack("Horny Aura", "", self.horny_aura), 
				Attack("Pizza box", "",  self.pizza_box), 
				Attack("Cheese spread", "", self.cheese_spread), 
				Attack("Greece shots", "", self.greece_shot), 
				Attack("Roasted to Perfection!", "", self.roasted_to_perfection), 
				Attack("Master of Comedy", "", self.master_of_comedy), 
				Attack("Flex", "", self.flex), 
				Attack("Retardation", "", self.retardation), 
				Attack("I can totally do this!", "", self.i_can_totally_do_this)
			],
			"MADDENED": [
				Attack("Waifu Smash", "", self.waifu_smash),
				Attack("Greece shots", "", self.greece_shot),
				Attack("Roasted to Perfection!", "", self.roasted_to_perfection), 
				Attack("I can totally do this!", "", self.i_can_totally_do_this)
			],
			"RELAXED": [
				Attack("Pizza box", "",  self.pizza_box), 
				Attack("Cheese spread", "", self.cheese_spread), 
				Attack("Flex", "", self.flex), 
			]
		}

		self.default_state = "NORMAL"
		self.state =  self.default_state


		# let this be 
		self.stacks = 0

	def get_info(self):
		return f"{self.get_other_info()}\n{self.get_stat_info()}"

	def get_other_info(self):
		return f"State - {self.state}"

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

	async def death(self, ctx, players):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_monster_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_monster_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_monster_info()}! They gained {self.exp_gives} experience points.")


	# ATTACKS

	async def waifu_smash(self, enemy, ctx, players, enemies, effects, client):
		# summons waifu who attacks the player dealing magic damage (magic only attack)
		await ctx.send("waifu smash")

	async def horny_aura(self, enemy, ctx, players, enemies, effects, client):
		# stuns player(s) for 1 move cuz of horniness
		pass

	async def pizza_box(self, enemy, ctx, players, enemies, effects, client):
		# summons massive cardboard box to protect itself for the next 2 turns(ups physical defense)
		pass

	async def cheese_spread(self, enemy, ctx, players, enemies, effects, client):
		# spreads lots of cheese over himself (ups def and mr)
		pass

	async def greece_shot(self, enemy, ctx, players, enemies, effects, client):
		# throws greece balls at player(s) cuz pizza never showers, doing physical damage
		pass

	async def roasted_to_perfection(self, enemy, ctx, players, enemies, effects, client):
		# converts the room into an oven dealing more and more physical damage over 3 turns
		pass

	async def master_of_comedy(self, enemy, ctx, players, enemies, effects, client):
		# makes the player(s) cringe incredibly hard with his bad joke (lowers player defense (both physical and magical))
		pass

	async def flex(self, enemy, ctx, players, enemies, effects, client):
		# flexes his pen spinning techniques, sadly impressing nobody. (lowers own def and mr)
		pass

	async def retardation(self, enemy, ctx, players, enemies, effects, client):
		# makes the player(s) retarded. The player(s) use a random ability in their next turn.
		pass

	async def i_can_totally_do_this(self, enemy, ctx, players, enemies, effects, client):
		# charges towards the player(s) looking incredibly cool. Trips on a banana peel and loses half remaining hp.
		pass