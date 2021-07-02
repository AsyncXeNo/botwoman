import random
class Player(object):
	def __init__(self, user_id, character_class, name):										
		self.user_id = user_id
		self.character_class = character_class
		self.name = name

	def __str__(self):
		return f"Name- {self.name}\nId- {self.user_id}\nClass- {self.character_class}"


class Pizza(Enemy):
	TYPES = ["SMALL", "MEDIUM", "LARGE", "THE EMBODIMENT OF DEGENERACY"]
	TYPE_TO_STATS = {
		"SMALL": {
			""
		}
	}
	def __init__(self, type_="MEDIUM"):
		self.type = type_

		self.validate()

	def get_info(self):
		return f"{self.type.title()} Pizza"

	def validate(self):
		if not (self.type.upper() in self.TYPES):
			raise Exception("invalid pizza type.")


class Enemy(object):
	TYPES = ["PHYSICAL", "MAGIC", "MIXED"]
	def __init__(self, maxhp, type_, physical, magic, def_, mag_def, agility):
		self.maxhp = maxhp,
		self.physical = physical
		self.magic = magic
		self.defense = def_
		self.magic_def = mag_def,
		self.agility = agility

		self.validate_type()

	def validate_type(self):
		if not (self.type.upper() in self.TYPES):
			raise Exception("invalid enemy type.")

		if self.type.upper() == "PHYSICAL":
			self.magic = 0
		elif self.type.upper() == "MAGIC":
			self.physical = 0
