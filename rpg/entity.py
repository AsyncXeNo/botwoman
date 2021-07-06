import random

from utils.logger import Logger

customlogger = Logger("rpg/entity.py")


class Entity(object):
	ENTITYTYPES = ["PHYSICAL", "MAGICAL", "MIXED"]
	def __init__(self, maxhp, entitytype, physical, magic, def_, mag_def, agility):
		self.maxhp = maxhp
		self.hp = self.maxhp
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


	# imp

	def gain_hp(self, hp):
		pass

	def deal_physcial(self, dmg):
		pass

	def deal_magical(self, dmg):
		pass

	def buff_physcial(self, buff):
		pass

	def debuff_physcial(self, debuff):
		pass

	def buff_magical(self, buff):
		pass

	def debuff_magical(self, debuff):
		pass

	def buff_armor(self, buff):
		pass

	def debuff_armor(self, debuff):
		pass

	def buff_mr(self, buff):
		pass

	def debuff_mr(self, debuff):
		pass

	def buff_agility(self, buff):
		pass

	def debuff_agility(self, debuff):
		pass
