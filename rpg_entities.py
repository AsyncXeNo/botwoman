import random
import copy
import json



# ------------------------------------------------- PLAYERS --------------------------------------------------------

class Player(object):
	PLAYERCLASSES = ["MAGE", "FIGHTER", "ASSASSIN", "HEALER"]
	def __init__(self, user_id, character_class, name):										
		self.user_id = user_id
		self.character_class = character_class
		self.name = name

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}"



# -------------------------------------------------- EMEMIES -------------------------------------------------------

class Enemy(object):
	ENEMYTYPES = ["PHYSICAL", "MAGICAL", "MIXED"]
	def __init__(self, maxhp, enemytype, physical, magic, def_, mag_def, agility):
		self.maxhp = maxhp
		self.physical = physical
		self.magic = magic
		self.defense = def_
		self.magic_def = mag_def
		self.agility = agility/100

		self.enemytype = enemytype

		self.validate_type()

	def validate_type(self):

		if self.enemytype <0 or self.enemytype >2 or (not (type(self.enemytype) == int)):
			print(f"This is gonna cause an Exception - {self.enemytype}")
			raise Exception("invalid enemy type.")

		self.enemytype = self.ENEMYTYPES[self.enemytype]

		if self.enemytype.upper() == "PHYSICAL":
			self.magic = 0
		elif self.enemytype.upper() == "MAGICAL":
			self.physical = 0

	def get_stat_info(self):
		return f"*MAX HP ->* `{self.maxhp}`\n*PHYSICAL DAMAGE ->* `{self.physical}`\n*MAGICAL DAMAGE ->* `{self.magic}`\n*PHYSICAL DEFENSE ->* `{self.defense}`\n*MAGIC DEFENSE ->* `{self.magic_def}`\n*AGILITY ->* `{self.agility}`"


class Pizza(Enemy):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	PIZZATYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]
	PIZZASTATES = ["NORMAL", "MADDENED", "RELAXED"]

	def __init__(self, pizzatype="MEDIUM"):
		self.pizzatype = pizzatype.upper()
		self.validate()

		self.stats = copy.copy(self.STATS[self.pizzatype])
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])

		Enemy.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])


		self.attacks = {
			"NORMAL": [self.degeneracy_blade, self.waifu_smash, self.horny_aura, self.pizza_box, self.cheese_spread, self.greece_shot, self.roasted_to_perfection, self.master_of_comedy, self.flex, self.retardation, self.i_can_totally_do_this],
			"MADDENED": [self.waifu_smash, self.greece_shot, self.roasted_to_perfection, self.i_can_totally_do_this],
			"RELAXED": [self.pizza_box, self.cheese_spread, self.flex],
			"STUNNED": []
		}

		self.default_state = "STUNNED"
		self.state =  self.default_state

	def get_info(self):
		return f"**{self.pizzatype.title()} Pizza**\n{self.get_stat_info()}"

	def get_pizza_info(self):
		return f"**{self.pizzatype.title()} Pizza**"

	def validate(self):
		if not (self.pizzatype in self.PIZZATYPES):
			raise Exception("invalid pizza type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.PIZZASTATES):
			raise Exception("invalid pizza state.")

		self.state = new_state.upper()

	async def attack(self, ctx, player):
		options = self.attacks[self.state]
		if len(options) == 0:
			await ctx.send(f"{self.get_pizza_info()} is currently ***{self.state}*** and cannot attack!")
			return
		attack = random.choice(options)
		attack(ctx, player)
		await ctx.send(attack)


	# ATTACKS

	def degeneracy_blade(self, ctx, player):
		# removes player(s) agility by making them fat
		pass

	def waifu_smash(self, ctx, player):
		# summons waifu who attacks the player dealing magic damage (magic only attack)
		pass

	def horny_aura(self, ctx, player):
		# stuns player(s) for 1 move cuz of horniness
		pass

	def pizza_box(self, ctx, player):
		# summons massive cardboard box to protect itself (ups physical defense)
		pass

	def cheese_spread(self, ctx, player):
		# spreads lots of cheese over himself (ups magic resist)
		pass

	def greece_shot(self, ctx, player):
		# throws greece balls at player(s) cuz pizza never showers, doing physical damage
		pass

	def roasted_to_perfection(self, ctx, player):
		# converts the room into an oven dealing more and more physical damage over 3 turns
		pass

	def master_of_comedy(self, ctx, player):
		# makes the player(s) cringe incredibly hard with his bad joke (lowers player defense (both physical and magical))
		pass

	def flex(self, ctx, player):
		# flexes his pen spinning techniques, sadly impressing nobody. (lowers own def and mr)
		pass

	def retardation(self, ctx, player):
		# makes the player(s) retarded. The player(s) use a random ability in their next turn.
		pass

	def i_can_totally_do_this(self, ctx, player):
		# charges towards the player(s) looking incredibly cool. Trips on a banana peel and loses half remaining hp.
		pass