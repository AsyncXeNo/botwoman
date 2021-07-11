from utils.logger import Logger
from rpg.items.item import Item
from rpg.entity import Entity
from rpg.battle import Battle


class ActiveItem(Item):
    def __init__(self, name:str, description:str, level:int, func:function):
        self.logger = Logger("rpg/items/active_item")
        super().__init__(name, description, level)

        self.func = func

        self.entity = None
        self.battle = None

    def get_entity(self):
        return self.entity

    def set_entity(self, entity:Entity):
        self.entity = entity

    def get_battle(self):
        return self.battle

    def set_battle(self, battle:Battle):
        self.battle = battle

    def clear(self):
        self.entity = None
        self.battle = None

    def use(self):
        if not self.entity:
            self.logger.log_error(f"Attempt to use {self.name}'s active when it has no entity assigned. Id- {self.id}")
            raise Exception(f"Attempt to use {self.name}'s active when it has no entity assigned. Id- {self.id}")
        
        if not self.battle:
            self.logger.log_error(f"Attempt to use {self.name}'s active when it has no battle assigned. Id- {self.id}")
            raise Exception(f"Attempt to use {self.name}'s active when it has no battle assigned. Id- {self.id}")

        self.func(self.entity, self.battle)