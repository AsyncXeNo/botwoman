from utils.logger import Logger
from utils.id_generator import IdGenerator


class Entity(object):
    def __init__(self, name: str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float):
        self.logger = Logger("rpg/entity")

        self.id = IdGenerator.generate_id()
        self.name = name

        self.logger.log_neutral(f"Spawning an entity named {self.name} with id {self.id}.")

        self.basemaxhp = maxhp
        self.basestr = strength
        self.basemp = mp
        self.basearmor = armor
        self.basemr = mr
        self.baseagility = agility

        self.statuses = []

        self.validate()
        self.setup()

    def validate(self):
        if self.basemaxhp < 1:
            self.logger.log_error("Max HP cannot be lower than 1.")
            raise Exception("Max HP cannot be lower than 1.")

        if self.basestr < 0:
            self.logger.log_error("Base strength cannot be lower than 0")
            raise Exception("Base strength cannot be lower than 0")

        if self.basemp < 0:
            self.logger.log_error("Base MP cannot be lower than 0")
            raise Exception("Base MP cannot be lower than 0")

        if self.baseagility < 0.0 or self.baseagility > 1.0:
            self.logger.log_error("Base agility needs to be in range 0.0 - 1.0")
            raise Exception("Base agility needs to be in range 0.0 - 1.0")

    def setup(self):
        self.hp = self.basemaxhp
        self.str = self.basestr
        self.mp = self.basemp
        self.armor = self.basearmor
        self.mr = self.basemr
        self.agility = self.baseagility


    # util

    def get_maxhp(self):
        pass

    def set_maxhp(self, maxhp:int):
        pass

    def give_maxhp(self, maxhp:int):
        pass  
