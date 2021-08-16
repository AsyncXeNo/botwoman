from utils.id_generator import IdGenerator
from utils.my_logging import get_logger


logger = get_logger(__name__)


class Turn(object):
    def __init__(self, battle, num:int):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        logger.debug(f'Starting Turn with id {self.ID}.')
        self.battle = battle
        self.num = num

        self.setup()
        self.start()

    def get_id(self):
        return self.ID

    def get_num(self):
        return self.num

    def get_battle(self):
        return self.battle

    def setup(self):
        members = self.get_battle().get_player_party().get_members() + self.get_battle().get_enemy_party().get_members()
        self.order = sorted([member.get_agility() for member in members])

    def start(self):
        while len(self.order) != 0:
            entity = self.order.pop(0)
            entity.tick()
            pass    
            # yeah idk what to do here yet.
