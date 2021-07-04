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
			"WOMAN": [],
			"HEALER": [],
			"TANK": []
		}

		self.default_state = "NORMAL"
		self.state = self.default_state

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

	# mage
	



# -------------------------------------------------- EMEMIES -------------------------------------------------------




class Pizza(Entity):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	PIZZATYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]
	PIZZASTATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED"]

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
		if not (self.pizzatype in self.PIZZATYPES):
			raise Exception("Invalid pizza type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.PIZZASTATES):
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


class Nist(Entity):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	NISTTYPES = ["SMALL", "MEDIUM", "LARGE", "FEMI(NIST)"]
	NISTSTATES = ["NORMAL", "MADDENED", "RELAXED", "STUNNED"]
	
	def __init__(self, nisttype):
		self.nisttype = nisttype.upper()
		self.validate()

		self.stats = copy.copy(self.STATS[self.nisttype])
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])
		
		Entity.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])

		self.exp_gives = self.stats["exp"]

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
		if not (self.nisttype in self.NISTTYPES):
			raise Exception("Invalid nist type.")

	def change_state(self, new_state):
		if not (new_state.upper() in self.NISTSTATES):
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



# --------------------------------------------------- ROOMS --------------------------------------------------------


class Room(object):
	def __init__(self, pos, ctx, client):
		self.client = client
		self.ctx = ctx
		self.pos = pos
		self.parties = []
		self.enemy_parties = []
		self.items = []

	def get_party_by_owner_id(self, owner_id):
		for party in self.parties:
			if party[0].user_id == owner_id:
				return party

		raise Exception("party not found (Room class)")

	def add_party(self, owner):
		party = self.client.get_cog("RPG").get_party_by_owner_id(owner.user_id)
		self.parties.append(party)
		for player in party:
			player.set_room(self)

		self.setup(self.parties.index(party))

	def setup(self, index):
		# CALLED AT THE VERY START WHILE SETTING UP THE DUNGEON AND EVERY TIME SOMEONE CHANGES ROOMS

		count = 0
		average_lv = 0
		for player in self.parties[index]:
			count += 1
			average_lv += player.level

		if count != 0:
			average_lv //= count
		else:
			average_lv = 10

		if not len(self.parties[index]) == 0:
			enemy_count = random.randint(1, len(self.parties[index]))
			enemy_party = []
			for _ in range(enemy_count):
				enemy_party.append(Pizza(Pizza.PIZZATYPES[random.randint(0, average_lv//3)]))

			self.enemy_parties.append(enemy_party)

	def get_info(self):
		response = f"```python\n# <{self.pos[0]}, {self.pos[1]}>\n"
		for party in self.parties:
			party = [player.name for player in party]
			response += f"# PLAYER PARTY: {', '.join(party)}\n"

		for party in self.enemy_parties:
			party = [pizza.get_monster_info() for pizza in party]
			response += f"# ENEMY PARTY: {', '.join(party)}\n"

		response += "```"

		return response

	async def start_event(self, owner):
		party = self.get_party_by_owner_id(owner.user_id)
		index = self.parties.index(party)


		await self.ctx.send(f"`PARTY - {', '.join([player.name for player in party])}` is going to fight `PARTY - {', '.join([pizza.get_monster_info() for pizza in self.enemy_parties[index]])}`!")
		await self.ctx.send("PRETEND THIS IS AN EVENT PLS OK GOOD")





		# very end
		index = self.parties.index(party)
		self.parties.remove(self.parties[index])
		self.enemy_parties.remove(self.enemy_parties[index])

		await self.client.get_cog("RPG_GAME").move_party(self.ctx, party)

