from utils.id_generator import IdGenerator
from utils.logger import Logger
from rpg.entity import Entity
from rpg.battle import Battle


class Ability(object):
    def __init__(self, name:str, description:str, entity:Entity, func:function, check:function):
        self.logger = Logger("rpg/ability")

        self.id = IdGenerator.generate_id()
        self.name = name
        self.description = description
        self.entity = entity
        self.func = func
        self.check = check
        
        self.battle = None
        
        return self.id

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

    def can_use(self):
        if not self.battle:
            self.logger.log_error("Checking if you can use an ability when not in combat?")
            raise Exception("Checking if you can use an ability when not in combat?")

        return self.check(self.entity)

    def use(self):
        if not self.check(self.entity):
            self.logger.log_error("How did it bypass the first check? You cannot use this ability right now.")
            raise Exception("How did it bypass the first check? You cannot use this ability right now.")

        if not self.battle:
            self.logger.log_error("Using an ability when not in combat?")
            raise Exception("Using an ability when not in combat?")
            
        self.func(self.entity, self.battle)