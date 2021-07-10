from utils.logger import Logger
from utils.id_generator import IdGenerator
from rpg.ability import Ability
from rpg.battle import Battle
from rpg.statuses.status import Status


class Entity(object):
    def __init__(self, name: str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float, stacks_name:str, abilities:list):
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
        self.stacks_name = stacks_name

        self.baseabilities = abilities

        self.statuses = []
        self.stacks = 0

        self.incombat = False

        self.items = {"active": [], "passive": []}

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

        for ability in self.abilities:
            if type(ability) != Ability:
                self.logger.log_error("Invalid ability.")
                raise Exception("Invalid ability.")

    def setup(self, battle):
        self.hp = self.basemaxhp
        self.str = self.basestr
        self.mp = self.basemp
        self.armor = self.basearmor
        self.mr = self.basemr
        self.agility = self.baseagility

        self.statuses = []
        self.stacks = 0

        for ability in self.baseabilities:
            ability.set_battle(battle)

        for item in self.items["active"]:
            item.set_entity(self)
            item.set_battle(battle)

    def ready_for_battle(self, battle):
        self.setup(battle)
        self.incombat = True

    def end_battle(self):
        for ability in self.baseabilities:
            ability.clear()

        for item in self.items["active"]:
            item.clear()
        
        self.incombat = False

    def get_name(self):
        return self.name

    def set_name(self, name:str):
        self.logger.log_neutral(f"Changing {self.id} entity's name from {self.name} to {name}")
        self.name = name

    def get_id(self):
        return self.id


    # base

    def get_maxhp(self):
        pass

    def set_maxhp(self, maxhp:int):
        pass

    def give_maxhp(self, maxhp:int):
        pass  

    def get_basestr(self):
        pass

    def set_basestr(self, strength:int):
        pass

    def give_basestr(self, strength:int):
        pass

    def get_basemp(self):
        pass

    def set_basemp(self, mp:int):
        pass

    def give_basemp(self, mp:int):
        pass

    def get_basearmor(self):
        pass

    def set_basearmor(self, armor:int):
        pass

    def give_basearmor(self, armor:int):
        pass

    def get_basemr(self):
        pass
    
    def set_basemr(self, mr:int):
        pass

    def give_basemr(self, mr:int):
        pass

    def get_baseagility(self):
        pass

    def set_baseagility(self, agility:float):
        pass

    def give_baseagility(self, agolity:float):
        pass

    def get_abilities(self):
        pass

    def set_abilities(self, abilities:list):
        pass

    def give_ability(self, ability:Ability):
        pass

    def take_ability(self, ability_id:str):
        pass


    # battle

    def tick(self):
        # all important pre-turn stuff.
        pass

    def in_combat(self):
        return self.in_combat

    def get_hp(self):
        pass

    def set_hp(self, hp:int):
        pass

    def give_hp(self, hp:int):
        pass  

    def get_str(self):
        pass

    def set_str(self, strength:int):
        pass

    def give_str(self, strength:int):
        pass

    def get_mp(self):
        pass

    def set_mp(self, mp:int):
        pass

    def give_mp(self, mp:int):
        pass

    def get_armor(self):
        pass

    def set_armor(self, armor:int):
        pass

    def give_armor(self, armor:int):
        pass

    def get_mr(self):
        pass
    
    def set_mr(self, mr:int):
        pass

    def give_mr(self, mr:int):
        pass

    def get_agility(self):
        pass

    def set_agility(self, agility:float):
        pass

    def give_agility(self, agility:float):
        pass

    def get_statuses(self):
        pass

    def set_statuses(self, statuses:list):
        pass

    def give_status(self, status:Status):
        pass

    def take_status(self, status_id:str):
        pass

    def get_stacks(self):
        pass

    def set_stacks(self, stacks:int):
        pass

    def give_stacks(self, stacks:int):
        pass

    def get_stacks_name(self):
        return self.stacks_name

    def set_stacks_name(self, name:str):
        self.logger.log_neutral(f"Stacks for entity {self.id} are now called {name}. (changed from {self.stacks_name})")
        self.stacks_name = name

    def get_usable_abilities(self, battle:Battle):
        pass