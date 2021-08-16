from rpg.entity import Entity
from utils.my_logging import get_logger


logger = get_logger(__name__)


class Enemy(Entity):
    def __init__(self, name: str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float, stacks_name: str, abilities: list, level: int):
        super().__init__(name, None, maxhp, strength, mp, armor, mr, agility, stacks_name, abilities)

        self.level = level

        # states (maybe later)

    def get_level(self):
        return self.level