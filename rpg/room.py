from rpg.parties.enemy_party import EnemyParty
from rpg.parties.player_party import PlayerParty
from utils.id_generator import IdGenerator
from utils.my_logging import get_logger
from utils.math import Vector2


logger = get_logger(__name__)


class Room(object):
    def __init__(self, pos:Vector2):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        logger.debug(f'Generating Room with ID {self.ID}.')
        self.pos = pos
        self.parties = {}

    def get_id(self):
        return self.ID

    def get_pos(self):
        return self.pos

    def add_party(self, party:PlayerParty):
        self.parties[party] = EnemyParty()