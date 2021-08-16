from utils.id_generator import IdGenerator
from utils.my_logging import get_logger


logger = get_logger(__name__)


class Ability(object):
    def __init__(self, name:str, description:str, entity, func, check):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        self.name = name
        self.description = description
        self.entity = entity
        self.func = func
        self.check = check
        
        self.battle = None

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_battle(self):
        return self.battle

    def set_battle(self, battle):
        self.battle = battle

    def clear(self):
        self.battle = None

    def can_use(self):
        if not self.battle:
            logger.error("Checking if you can use an ability when not in combat?")
            raise Exception("Checking if you can use an ability when not in combat?")

        return self.check(self.entity)

    def use(self):
        if not self.check(self.entity):
            logger.error("How did it bypass the first check? You cannot use this ability right now.")
            raise Exception("How did it bypass the first check? You cannot use this ability right now.")

        if not self.battle:
            logger.error("Using an ability when not in combat?")
            raise Exception("Using an ability when not in combat?")
            
        self.func(self.entity, self.battle)