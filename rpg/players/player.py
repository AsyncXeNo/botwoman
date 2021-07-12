from rpg.entity import Entity
from utils.logger import Logger


class Player(Entity):
    def __init__(self, name: str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float, stacks_name:str, abilities:list):
        self.logger = Logger("rpg/players/player")

        super().__init__(name, maxhp, strength, mp, armor, mr, agility, stacks_name, abilities)

        self.level = 1
        self.exp = 0
        self.exp_to_lv_up = 100

    def get_level(self):
        return self.level

    def level_up(self):
        pass
        
    def deal_physical(self, damage: int):
        self.error_if_not_in_combat()
        if self.get_armor() == 0:
            self.take_hp(damage)
            return

        reduction = 1 - (5099 / (self.get_level() * self.get_armor() + 5098))
        damage = int(damage - (damage*reduction))
        self.take_hp(damage)

    def deal_magical(self, damage: int):
        self.error_if_not_in_combat()
        if self.get_mr() == 0:
            self.take_hp(damage)
            return
        
        reduction = 1 - (5099 / (self.get_level() * self.get_mr() + 5098))
        damage = int(damage - (damage*reduction))
        self.take_hp(damage)
