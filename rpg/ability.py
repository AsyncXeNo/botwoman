from utils.logger import Logger
from rpg.entity import Entity
from rpg.battle import Battle


class Ability(object):
    def __init__(self, entity:Entity, func:function):
        self.logger = Logger("rpg/ability")

        self.entity.entity
        self.battle = None

    def get_battle(self):
        return self.battle

    def set_battle(self, battle:Battle):
        self.battle = battle

    def clear(self):
        self.battle = None

    def use(self):
        if not self.battle:
            self.logger.log_error("Using an ability when not in combat?")
            raise Exception("Using an ability when not in combat?")
            
        self.func(self.entity, self.battle)