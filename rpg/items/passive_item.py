from utils.logger import Logger
from rpg.items.item import Item
from rpg.entity import Entity


class PassiveItem(Item):
    def __init__(self, name:str, description:str, level:str, permanent:bool, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float):
        self.logger = Logger("rpg/items/passive_item")

        super().__init__(name, description, level)

        self.permanent = permanent

        self.maxhp = maxhp
        self.str = strength
        self.mp = mp
        self.armor = armor
        self.mr = mr
        self.agility = agility

        self.entity = None
    
    def is_permanent(self):
        return self.permanent    

    def get_entity(self):
        return self.entity

    def set_entity(self, entity:Entity):
        self.entity = entity

    def clear(self):
        if self.is_permanent():
            self.logger.log_alert(f"This is a permanent item and hence cannot be removed. Name - {self.get_name()} Id - {self.get_id()}")
            return
        self.entity = None