from rpg.entity import Entity
from utils.my_logging import get_logger


logger = get_logger(__name__)


class Player(Entity):
    def __init__(self, name: str, player_id:str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float, stacks_name:str, abilities:list):
        super().__init__(name, player_id, maxhp, strength, mp, armor, mr, agility, stacks_name, abilities)

        self.level = 1
        self.exp = 0
        self.exp_to_lv_up = 100

    def get_level(self):
        return self.level

    def get_exp(self):
        return self.exp

    def level_up(self):
        if self.get_level() == self.max_lv:
            logger.warn(f"{self.get_name()} is already max level.")
            return f"{self.get_name()} is already max level."

        maxhp = self.basemaxhp
        strength = self.basestr
        mp = self.basemp
        armor = self.basearmor
        mr = self.basemr
        agility = self.baseagility

        self.give_maxhp(maxhp*0.3)
        self.give_basestr(strength*0.3)
        self.give_basemp(mp*0.3)
        self.give_basearmor(armor*0.3)
        self.give_basemr(mr*0.3)
        self.give_baseagility(agility*0.3)
        self.exp_to_lv_up = self.exp_to_lv_up * 1.3

        self.level += 1

        return f"{self.name} leveled up! ({self.level-1} -> {self.level})\nMax HP {maxhp} -> {self.basemaxhp}\nStrength {strength} -> {self.basestr}\nMP {mp} -> {self.basemp}\nArmor {armor} -> {self.basearmor}\nMR {mr} -> {self.basemr}\nAgility {agility} -> {self.baseagility}"

    def give_exp(self, exp:int):
        if self.exp + exp > self.exp_to_lv_up:
            exp_left = exp - self.exp_to_lv_up
            self.level_up()
            self.give_exp(exp_left)
