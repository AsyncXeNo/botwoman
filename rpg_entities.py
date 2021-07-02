import random
import json


class Player(object):
	def __init__(self, user_id, character_class, name):										
		self.user_id = user_id
		self.character_class = character_class
		self.name = name

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}"


class Enemy(object):
	ENEMYTYPES = ["PHYSICAL", "MAGICAL", "MIXED"]
	def __init__(self, maxhp, enemytype, physical, magic, def_, mag_def, agility):
		self.maxhp = maxhp,
		self.physical = physical
		self.magic = magic
		self.defense = def_
		self.magic_def = mag_def,
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
		return f"MAX HP - {self.maxhp}\nPHYSICAL DAMAGE - {self.physical}\nMAGICAL DAMAGE - {self.magic}\nPHYSICAL DEFENSE - {self.defense}\nMAGIC DEFENSE - {self.magic_def}\nAGILITY - {self.agility}"


class Pizza(Enemy):
	with open("res/rpg/pizzastats.json", "r") as f:
		STATS = json.load(f)

	PIZZATYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]

	def __init__(self, pizzatype="MEDIUM"):
		self.pizzatype = pizzatype.upper()
		self.validate()

		self.stats = self.STATS[pizzatype]
		for stat in self.stats:
			self.stats[stat] = random.randint(self.stats[stat][0], self.stats[stat][1])

		Enemy.__init__(self, self.stats["maxhp"], self.stats["type"], self.stats["physical"], self.stats["magic"],self.stats["defense"], self.stats["magic_def"], self.stats["agility"])

	def get_info(self):
		return f"**{self.pizzatype.title()} Pizza**\n{self.get_stat_info()}"

	def validate(self):
		if not (self.pizzatype in self.PIZZATYPES):
			raise Exception("invalid pizza type.")
