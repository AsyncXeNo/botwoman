import random

from rpg.enemies.pizza import Pizza
from rpg.enemies.nist import Nist
from rpg.battle_manager import Battle_Manager
from utils.logger import Logger

customlogger = Logger("rpg/room.py")


class Room(object):
	ENEMYCLASSES = [Pizza, Nist]
	def __init__(self, pos, ctx, client):
		self.client = client
		self.ctx = ctx
		self.battle_manager = Battle_Manager(self)
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
			enemy_count = len(self.parties[index])
			enemy_party = []
			for _ in range(enemy_count):
				Enemy_class = random.choice(self.ENEMYCLASSES)
				enemy_party.append(Enemy_class(Enemy_class.TYPES[random.randint(0, average_lv//3)]))

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

		customlogger.log_neutral(f"Party index - {index}")
		await self.battle_manager.start_battle(index)

		# very end
		index = self.parties.index(party)
		self.parties.remove(self.parties.index(party))
		self.enemy_parties.remove(self.parties.index(party))

		await self.client.get_cog("RPG_GAME").move_party(self.ctx, party)
