import random
import copy
import json


class Entity(object):
	ENTITYTYPES = ["PHYSICAL", "MAGICAL", "MIXED"]
	def __init__(self, maxhp, entitytype, physical, magic, def_, mag_def, agility):
		self.maxhp = maxhp
		self.physical = physical
		self.magic = magic
		self.defense = def_
		self.magic_def = mag_def
		self.agility = agility/100

		self.entitytype = entitytype

		self.validate_type()

	def validate_type(self):

		if self.entitytype <0 or self.entitytype >2 or (not (type(self.entitytype) == int)):
			raise Exception("invalid enemy type.")

		self.entitytype = self.ENTITYTYPES[self.entitytype]

		if self.entitytype.upper() == "PHYSICAL":
			self.magic = None
		elif self.entitytype.upper() == "MAGICAL":
			self.physical = None

	def get_stat_info(self):
		return f"*MAX HP ->* `{self.maxhp}`\n*PHYSICAL DAMAGE ->* `{self.physical}`\n*MAGICAL DAMAGE ->* `{self.magic}`\n*PHYSICAL DEFENSE ->* `{self.defense}`\n*MAGIC DEFENSE ->* `{self.magic_def}`\n*AGILITY ->* `{self.agility}\n`"


# ------------------------------------------------- PLAYERS --------------------------------------------------------


class Player(Entity):
	PLAYERCLASSES = ["MAGE", "FIGHTER", "ASSASSIN", "HEALER"]
	PLAYERSTATES = ["NORMAL", "STUNNED"]
	def __init__(self, user_id, character_class, name):										
		self.user_id = user_id
		self.character_class = character_class
		self.name = name

		self.level = 1
		self.exp = 0

		self.attacks = {
			"MAGE": [],
			"FIGHTER": [],
			"ASSASSIN": [],
			"HEALER": []
		}

		self.default_state = "NORMAL"
		self.state = self.default_state

	def change_state(self, new_state):
		if not (new_state.upper() in self.PLAYERSTATES):
			raise Exception("Invalid player state.")

		self.state = new_state.upper()

	async def attack(self, ctx, enemies):
		if self.state.upper() == "STUNNED":
			await ctx.send(f"**{self.name}** is currently ***{self.state}*** and cannot attack!")

	async def give_exp(self, ctx, exp):
		await ctx.send(f"**{self.name}** you just gained {exp} experience points!")

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}"


	# ATTACKS





# -------------------------------------------------- EMEMIES -------------------------------------------------------




class Pizza(Entity):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	PIZZATYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]
	PIZZASTATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED"]

	def __init__(self, pizzatype="MEDIUM"):
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

	def get_pizza_info(self):
		return f"**{self.pizzatype.title()} Pizza**"

	def validate(self):
		if not (self.pizzatype in self.PIZZATYPES):
			raise Exception("Invalid pizza type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.PIZZASTATES):
			raise Exception("Invalid pizza state.")

		self.state = new_state.upper()

	async def attack(self, ctx, players):
		if self.state.upper() == "STUNNED":
			await ctx.send(f"{self.get_pizza_info()} is currently ***{self.state}*** and cannot attack!")
			return

		options = self.attacks[self.state]
		attack = random.choice(options)
		attack(ctx, players)
		await ctx.send(attack)

	async def death(self, ctx, players):
		players = [f"**{player.name}**" for player in players]
		if len(players) > 2:
			await ctx.send(f"{(', ').join(players[:-1])} and {players[-1]} have slain {self.get_pizza_info()}! All of them gained {self.exp_gives//len(players)} exp points.")

		elif len(players) == 2:
			await ctx.send(f"{(' and ').join(players)} have slain {self.get_pizza_info()}! Both of them gained {self.exp_gives//len(players)} experience points.")

		else:
			await ctx.send(f"{players[0]} has slain {self.get_pizza_info()}! They gained {self.exp_gives} experience points.")


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
		# summons massive cardboard box to protect itself (ups physical defense)
		pass

	def cheese_spread(self, ctx, players):
		# spreads lots of cheese over himself (ups magic resist)
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


# --------------------------------------------------- ROOMS --------------------------------------------------------


class Room(object):
	def __init__(self, pos):
		self.pos = pos
		self.players = []
		self.enemies = []
		self.items = []

	def add_player(self, player):
		self.players.append(player)

	def setup(self):
		# CALLED AT THE VERY START WHILE SETTING UP THE DUNGEON AND EVERY TIME SOMEONE CHANGES ROOMS
		if not len(self.players) == 0:
			enemy_count = random.randint(1, len(self.players))
			for enemy in range(enemy_count):
				self.enemies.append(Pizza(random.choice(Pizza.PIZZATYPES)))

	def get_info(self):
		response = f"{'-'*50}\n{self.pos}\nPLAYERS:\n"
		for player in self.players:
			response += player.__str__()

		response += "\nENEMIES:\n"
		for enemy in self.enemies:
			response += enemy.get_info()

		response += f"{'-'*50}\n"

		return response