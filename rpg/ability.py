from utils.logger import Logger
from rpg.entity import Entity
from rpg.battle import Battle


class Ability(object):
    def __init__(self, name:str, description:str, entity:Entity, func:function):
        self.logger = Logger("rpg/ability")

        self.name = name
        self.description = description
        self.entity = entity
        self.func = func
        
        self.battle = None

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

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