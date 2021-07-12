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
        self.add_buffs()

    def clear(self):
        if self.is_permanent():
            self.logger.log_alert(f"This is a permanent item and hence cannot be removed. Name - {self.get_name()} Id - {self.get_id()}")
            return
        self.remove_buffs()
        self.entity = None

    def add_buffs(self):
        if not self.entity:
            self.logger.log_error(f"Adding buffs to something that does not exist? name - {self.name} id - {self.id}")
            raise Exception("Adding buffs to something that does not exist? name - {self.name} id - {self.id}")

        self.entity.give_maxhp(self.maxhp)
        self.entity.give_str(self.str)
        self.entity.give_mp(self.mp)
        self.entity.give_armor(self.armor)
        self.entity.give_mr(self.mr)
        self.entity.give_agility(self.agility)

    def remove_buffs(self):
        if not self.entity:
            self.logger.log_error(f"Removing buffs from something that does not exist? name - {self.name} id - {self.id}")
            raise Exception("Removing buffs from something that does not exist? name - {self.name} id - {self.id}")

        self.entity.give_maxhp(-self.maxhp)
        self.entity.give_str(-self.str)
        self.entity.give_mp(-self.mp)
        self.entity.give_armor(-self.armor)
        self.entity.give_mr(-self.mr)
        self.entity.give_agility(-self.agility)