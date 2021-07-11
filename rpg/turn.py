from utils.id_generator import IdGenerator
from utils.logger import Logger
from rpg.parties.player_party import PlayerParty
from rpg.parties.enemy_party import EnemyParty
from rpg.players.player import Player
from rpg.enemies.enemy import Enemy
from rpg.statuses.status import Status
from rpg.battle import Battle


class Turn(object):
    def __init__(self, battle:Battle, num:int):
        self.logger = Logger("rpg/turn")

        self.id = IdGenerator.generate_id()
        self.battle = battle
        self.num = num

        self.setup()
        self.start()

        return self.id

    def get_id(self):
        return self.id

    def get_num(self):
        return self.num

    def get_battle(self):
        return self.battle

    def setup(self):
        members = self.get_battle().get_player_party().get_members() + self.get_battle().get_enemy_party().get_members()
        self.order = sorted([member.get_agility() for member in members])

    def start(self):
        pass
        
        # yeah idk what to do here yet.
