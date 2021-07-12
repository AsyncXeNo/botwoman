from rpg.parties.enemy_party import EnemyParty
from rpg.parties.player_party import PlayerParty
from utils.id_generator import IdGenerator
from utils.logger import Logger
from utils.math import Vector2


class Room(object):
    def __init__(self, pos:Vector2):
        self.logger = Logger("rpg/room")
        
        self.id = IdGenerator.generate_id()
        self.pos = pos

        self.parties = {}

    def get_id(self):
        return self.id

    def get_pos(self):
        return self.pos

    def add_party(self, party:PlayerParty):
        self.parties[party] = EnemyParty()