from utils.logger import Logger
from utils.id_generator import IdGenerator
from rpg.ability import Ability
from rpg.battle import Battle
from rpg.items.active_item import ActiveItem
from rpg.items.passive_item import PassiveItem
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
        self.battle = None

        self.items = {"active": [], "passive": []}

        self.validate()
        self.setup()

        return self.id

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
        if self.in_combat():
            self.logger.log_error("Cannot setup while already in combat.")
            raise Exception("Cannot setup while already in combat.")

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
        self.battle = battle
        self.incombat = True

    def end_battle(self):
        if not self.in_combat():
            self.logger.log_error("Cannot end a battle which has not started yet.")
            raise Exception("Cannot end a battle which has not started yet.")

        for ability in self.baseabilities:
            ability.clear()

        for item in self.items["active"]:
            item.clear()
        
        self.incombat = False
        self.battle = None

    def get_name(self):
        return self.name

    def set_name(self, name:str):
        if self.in_combat():
            self.logger.log_error("Cannot change name while in combat.")
            raise Exception("Cannot change name while in combat.")
        self.logger.log_neutral(f"Changing {self.id} entity's name from {self.name} to {name}")
        self.name = name

    def get_id(self):
        return self.id


    # base

    def error_if_in_combat(self):
        if not self.in_combat():
            self.logger.log_error("Called a function which can only be called when not in battle.")
            raise Exception("Called a function which can only be called when not in battle.")

    def get_maxhp(self):
        if self.basemaxhp < 1:
            return 1
        return self.basemaxhp

    def set_maxhp(self, maxhp:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of maxhp to {maxhp}. I hope you know what you're doing because this process is irreversible.")
        self.basemaxhp = maxhp

    def give_maxhp(self, maxhp:int):
        self.error_if_in_combat()
        self.basemaxhp += maxhp

    def get_basestr(self):
        if self.basestr < 0:
            return 0
        return self.basestr

    def set_basestr(self, strength:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base strength to {strength}. I hope you know what you're doing because this process is irreversible.")
        self.basestr = strength

    def give_basestr(self, strength:int):
        self.error_if_in_combat()
        self.basestr += strength

    def get_basemp(self):
        if self.basemp < 0:
            return 0   
        return self.basemp

    def set_basemp(self, mp:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base MP to {mp}. I hope you know what you're doing because this process is irreversible.")
        self.basemp = mp

    def give_basemp(self, mp:int):
        self.error_if_in_combat()
        self.basemp += mp

    def get_basearmor(self):
        if self.basearmor < 0:
            return 0
        return self.basearmor
    
    def set_basearmor(self, armor:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base armor to {armor}. I hope you know what you're doing because this process is irreversible.")
        self.basearmor = armor

    def give_basearmor(self, armor:int):
        self.error_if_in_combat()
        self.basearmor += armor

    def get_basemr(self):
        if self.basemr < 0:
            return 0
        return self.basemr

    def set_basemr(self, mr:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base MR to {mr}. I hope you know what you're doing because this process is irreversible.")
        self.basemr = mr

    def give_basemr(self, mr:int):
        self.error_if_in_combat()
        self.basemr += mr

    def get_baseagility(self):
        if self.baseagility < 0.0:
            return 0.0
        if self.baseagility > 1.0:
            return 1.0
        return self.baseagility

    def set_baseagility(self, agility:float):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base agility to {agility}. I hope you know what you're doing because this process is irreversible.")
        self.baseagility = agility

    def give_baseagility(self, agility:float):
        self.error_if_in_combat()
        self.baseagility += agility

    def get_abilities(self):
        return self.baseabilities

    def set_abilities(self, abilities:list):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the the abilities for the entity named {self.get_name()} with if {self.get_id()}. I hope you know what you're doing because this process is irreversible.")
        self.baseabilities= abilities

    def give_ability(self, ability:Ability):
        self.error_if_in_combat()
        self.baseabilities.append(ability)

    def take_ability(self, name:str):
        self.error_if_in_combat()
        self.baseabilities.remove(self.get_ability_by_name(name))

    def get_passive_items(self):
        return self.items["passive"]

    def give_passive_item(self, item:PassiveItem):
        self.error_if_in_combat()
        if self.in_combat():
            self.logger.log_error("Cannot add item while in combat.")
            raise Exception("Cannot add item while in combat.")
        self.items["passive"].append(item)
        item.set_entity(self)

    def remove_passive_item(self, name:str):
        self.error_if_in_combat()
        if self.in_combat():
            self.logger.log_error("Cannot remove item while in combat.")
            raise Exception("Cannot remove item while in combat.")
        item = self.get_passive_item_by_name(name)
        if item.is_permanet():
            self.logger.log_alert(f"Cannot remove item named {item.get_name()} cuz it is permanent")
            return f"Cannot remove item named {item.get_name()} cuz it is permanent"
        item.clear()
        self.items["passive"].remove(item)

    def get_active_items(self):
        return self.items["active"]

    def give_active_item(self, item:ActiveItem):
        self.error_if_in_combat()
        if self.in_combat():
            self.logger.log_error("Cannot add item while in combat.")
            raise Exception("Cannot add item while in combat.")
        self.items["active"].append(item)

    def remove_active_item(self, name:str):
        self.error_if_in_combat()
        if self.in_combat():
            self.logger.log_error("Cannot remove item while in combat.")
            raise Exception("Cannot remove item while in combat.")
        self.items["active"].remove(self.get_active_item_by_name(name))

    def get_stacks_name(self):
        return self.stacks_name

    def set_stacks_name(self, name:str):
        if self.in_combat():
            self.logger.log_error("Cannot change stacks name while in combat.")
            raise Exception("Cannot change stacks name while in combat.")
        self.logger.log_neutral(f"Stacks for entity {self.id} are now called {name}. (changed from {self.stacks_name})")
        self.stacks_name = name


    # battle

    def tick(self):
        # all important pre-turn stuff.
        pass

    def in_combat(self):
        return self.in_combat

    def error_if_not_in_combat(self):
        if not self.in_combat():
            self.logger.log_error("Called a function which can only be called while in battle.")
            raise Exception("Called a function which can only be called while in battle.")

    def get_hp(self):
        self.error_if_not_in_combat()
        return self.hp

    def set_hp(self, hp:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You are directly setting the HP of this entity to {hp}. I hope you know what you are doing cuz this process is irreversible.")
        self.hp = hp

    def give_hp(self, hp:int):
        pass  

    def get_str(self):
        self.error_if_not_in_combat()
        return self.str

    def set_str(self, strength:int):
        pass

    def give_str(self, strength:int):
        pass

    def deal_physical(self, damage:int):
        pass

    def get_mp(self):
        self.error_if_not_in_combat()
        return self.mp

    def set_mp(self, mp:int):
        pass

    def give_mp(self, mp:int):
        pass

    def deal_magical(self, damage:int):
        pass

    def get_armor(self):
        self.error_if_not_in_combat()
        return self.armor

    def set_armor(self, armor:int):
        pass

    def give_armor(self, armor:int):
        pass

    def get_mr(self):
        self.error_if_not_in_combat()
        return self.mr
    
    def set_mr(self, mr:int):
        pass

    def give_mr(self, mr:int):
        pass

    def get_agility(self):
        self.error_if_not_in_combat()
        return self.agility

    def set_agility(self, agility:float):
        pass

    def give_agility(self, agility:float):
        pass

    def get_statuses(self):
        self.error_if_not_in_combat()
        return self.statuses

    def set_statuses(self, statuses:list):
        pass

    def give_status(self, status:Status):
        pass

    def take_status(self, status_name:str):
        pass

    def get_stacks(self):
        return self.stacks

    def set_stacks(self, stacks:int):
        pass

    def give_stacks(self, stacks:int):
        pass

    def get_usable_abilities(self):
        pass

    def get_usable_items(self):
        pass

    def get_battle(self):
        if not self.in_combat():
            self.logger.log_alert("currently not in battle. get_battle() will return nothing")
        
        return self.battle


    # helper

    def get_passive_item_by_id(self, item_id:str):
        for item in self.items["passive"]:
            if item.get_id() == item_id:
                return item

        self.logger.log_alert(f"Item with id {item_id} not found in passive items.")

    def get_passive_item_by_name(self, name:str):
        for item in self.items["passive"]:
            if item.get_name() == name:
                return item

        self.logger.log_alert(f"Item with name {name} not found in passive items.")

    def get_active_item_by_id(self, item_id:str):
        for item in self.items["active"]:
            if item.get_id() == item_id:
                return item

        self.logger.log_alert(f"Item with id {item_id} not found in active items.")

    def get_active_item_by_name(self, name:str):
        for item in self.items["active"]:
            if item.get_name() == name:
                return item

        self.logger.log_alert(f"Item with name {name} not found in active items.")

    def get_status_by_id(self, status_id:str):
        for status in self.statuses:
            if status.get_id() == status_id:
                return status

        self.logger.log_alert(f"Status with id {status_id} not found in statuses.")

    def get_status_by_name(self, name:str):
        for status in self.statuses:
            if status.get_name() == name:
                return status

        self.logger.log_warning(f"Status with name {name} not found in statuses.")

    def get_ability_by_id(self, ability_id:str):
        for ability in self.get_abilities():
            if ability.get_id() == ability_id:
                return ability

        self.logger.log_alert(f"Ability with id {ability_id} not found in abilities.")

    def get_ability_by_name(self, name:str):
        for ability in self.get_abilities():
            if ability.get_name() == name:
                return ability

        self.logger.log_warning(f"Ability with name {name} not found in abilities.")