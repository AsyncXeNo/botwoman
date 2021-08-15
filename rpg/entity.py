from utils.logger import Logger
from utils.id_generator import IdGenerator
from rpg.ability import Ability
from rpg.battle import Battle
from rpg.items.active_item import ActiveItem
from rpg.items.passive_item import PassiveItem
from rpg.statuses.status import Status


class Entity(object):
    def __init__(self, name: str, entity_id:str, maxhp: int, strength: int, mp: int, armor: int, mr: int, agility: float, stacks_name:str, abilities:list):
        self.logger = Logger("rpg/entity")

        self.id = entity_id
        if not self.id:
            self.id = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
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
        self.turn = False
        self.battle = None

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

        for ability in self.baseabilities:
            if type(ability) != Ability:
                self.logger.log_error("Invalid ability.")
                raise Exception("Invalid ability.")

    def setup(self):
        self.hp = self.basemaxhp
        self.str = self.basestr
        self.mp = self.basemp
        self.armor = self.basearmor
        self.mr = self.basemr
        self.agility = self.baseagility

        self.statuses = []
        self.stacks = 0

    def ready_for_battle(self, battle:Battle):
        if self.in_combat():
            self.logger.log_error("Cannot ready for battle while already in combat.")
            raise Exception("Cannot ready for battle while already in combat.")

        self.setup(battle)

        for ability in self.baseabilities:
            ability.set_battle(battle)

        for item in self.items["active"]:
            item.set_entity(self)
            item.set_battle(battle)
            
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
        maxhp = self.basemaxhp
        for item in self.items["passive"]:
            maxhp += item.maxhp
        if maxhp < 1:
            return 1
        return maxhp

    def set_maxhp(self, maxhp:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of maxhp to {maxhp}. I hope you know what you're doing because this process is irreversible.")
        self.basemaxhp = maxhp

    def give_maxhp(self, maxhp:int):
        self.error_if_in_combat()
        self.basemaxhp += maxhp

    def get_basestr(self):
        basestr = self.basestr
        for item in self.items["passive"]:
            basestr += item.str
        if basestr < 0:
            return 0
        return basestr

    def set_basestr(self, strength:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base strength to {strength}. I hope you know what you're doing because this process is irreversible.")
        self.basestr = strength

    def give_basestr(self, strength:int):
        self.error_if_in_combat()
        self.basestr += strength

    def get_basemp(self):
        basemp = self.basemp
        for item  in self.items["passive"]:
            basemp += item.mp
        if basemp < 0:
            return 0   
        return basemp

    def set_basemp(self, mp:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base MP to {mp}. I hope you know what you're doing because this process is irreversible.")
        self.basemp = mp

    def give_basemp(self, mp:int):
        self.error_if_in_combat()
        self.basemp += mp

    def get_basearmor(self):
        basearmor = self.basearmor
        for item in self.items["passive"]:
            basearmor += item.armor
        if basearmor < 0:
            return 0
        return basearmor
    
    def set_basearmor(self, armor:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base armor to {armor}. I hope you know what you're doing because this process is irreversible.")
        self.basearmor = armor

    def give_basearmor(self, armor:int):
        self.error_if_in_combat()
        self.basearmor += armor

    def get_basemr(self):
        basemr = self.basemr
        for item in self.items["passive"]:
            basemr += item.mr
        if basemr < 0:
            return 0
        return basemr

    def set_basemr(self, mr:int):
        self.error_if_in_combat()
        self.logger.log_alert(f"You're directly setting the value of base MR to {mr}. I hope you know what you're doing because this process is irreversible.")
        self.basemr = mr

    def give_basemr(self, mr:int):
        self.error_if_in_combat()
        self.basemr += mr

    def get_baseagility(self):
        baseagility = self.baseagility
        for item in self.items["passive"]:
            baseagility += item.agility
        if baseagility < 0.0:
            return 0.0
        if baseagility > 1.0:
            return 1.0
        return baseagility

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

    def turn(self):
        return self.turn

    def set_turn_true(self):
        self.turn = True

    def set_turn_false(self):
        self.turn = False

    def error_if_not_in_combat(self):
        if not self.in_combat():
            self.logger.log_error("Called a function which can only be called while in battle.")
            raise Exception("Called a function which can only be called while in battle.")

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

    def deal_true(self, damage:int):
        self.take_hp(damage)

    def get_hp(self):
        self.error_if_not_in_combat()
        if self.hp <= 0:
            return 0
        return self.hp

    def set_hp(self, hp:int):
        self.error_if_not_in_combat()
        if hp < 0:
            self.logger.log_error("Cannot set HP to be directly lower than 0.")
            raise Exception("Cannot set HP to be directly lower than 0.")
        self.logger.log_alert(f"You are directly setting the HP of this entity to {hp}. I hope you know what you are doing cuz this process is irreversible and can bypass the maxhp filter.")
        self.hp = hp

    def give_hp(self, hp:int):
        self.error_if_not_in_combat()
        if hp < 0:
            self.logger.log_error("Please use deal_physcial or deal_magical if you want to damage the entity.")
            raise Exception("Please use deal_physcial or deal_magical if you want to damage the entity.")
        if self.hp + hp > self.get_maxhp:
            self.hp = self.get_maxhp
            return
        self.get_hp += hp 

    def take_hp(self, hp:int):
        self.error_if_not_in_combat()
        if self.hp - hp <= 0:
            self.hp = 0
            return
        self.hp -= hp

    def get_str(self):
        self.error_if_not_in_combat()
        return self.str

    def set_str(self, strength:int):
        self.error_if_not_in_combat()
        if strength < 0:
            self.logger.log_error("Cannot set strength to be lower than 0.")
            raise Exception("Cannot set strength to be lower than 0.")
        self.logger.log_alert(f"You are directly setting the STRENGTH of this entity to {strength}. I hope you know what you are doing cuz this process is irreversible.")
        self.str = strength

    def give_str(self, strength:int):
        self.error_if_not_in_combat()
        if self.str + strength < 0:
            self.str = 0
            return
        self.str += strength

    def get_mp(self):
        self.error_if_not_in_combat()
        return self.mp

    def set_mp(self, mp:int):
        self.error_if_not_in_combat()
        if mp < 0:
            self.logger.log_error("Cannot set MP to be lower than 0.")
            raise Exception("Cannot set MP to be lower than 0.")
        self.logger.log_alert(f"You are directly setting the MP of this entity to {mp}. I hope you know what you are doing cuz this process is irreversible.")
        self.mp = mp

    def give_mp(self, mp:int):
        self.error_if_not_in_combat()
        if self.mp + mp < 0:
            self.mp = 0
            return
        self.mp += mp

    def get_armor(self):
        self.error_if_not_in_combat()
        return self.armor

    def set_armor(self, armor:int):
        self.error_if_not_in_combat()
        if armor < 0:
            self.logger.log_error("Cannot set Armor to be lower than 0.")
            raise Exception(("Cannot set Armor to be lower than 0."))
        self.logger.log_alert(f"You are directly setting the armor of this entity to {armor}. I hope you know what you are doing cuz this process is irreversible.")
        self.armor = armor

    def give_armor(self, armor:int):
        self.error_if_not_in_combat()
        if self.armor + armor < 0:
            self.armor = 0
            return
        self.armor += armor

    def get_mr(self):
        self.error_if_not_in_combat()
        return self.mr
    
    def set_mr(self, mr:int):
        self.error_if_not_in_combat()
        if mr < 0:
            self.logger.log_error("Cannot set MR to be lower than 0.")
            raise Exception(("Cannot set MR to be lower than 0."))
        self.logger.log_alert(f"You are directly setting the MR of this entity to {mr}. I hope you know what you are doing cuz this process is irreversible.")
        self.mr = mr

    def give_mr(self, mr:int):
        self.error_if_not_in_combat()
        if self.mr + mr < 0:
            self.mr = 0
            return
        self.mr += mr

    def get_agility(self):
        self.error_if_not_in_combat()
        return self.agility

    def set_agility(self, agility:float):
        self.error_if_not_in_combat()
        if agility < 0.0:
            self.logger.log_error("Cannot set aglity to be lower than 0.")
            raise Exception(("Cannot set agility to be lower than 0."))
        if agility < 1.0:
            self.logger.log_error("Cannot set aglity to be more than 1.")
            raise Exception(("Cannot set agility to be lower than 0."))
        self.logger.log_alert(f"You are directly setting the agility of this entity to {agility}. I hope you know what you are doing cuz this process is irreversible.")
        self.agility = agility

    def give_agility(self, agility:float):
        self.error_if_not_in_combat()
        if self.agility + agility < 0.0:
            self.agility = 0.0
            return
        if self.agility + agility > 1.0:
            self.agility = 1.0
            return
        self.agility += agility

    def get_statuses(self):
        self.error_if_not_in_combat()
        return self.statuses

    def set_statuses(self, statuses:list):
        self.error_if_not_in_combat()
        for status in statuses:
            if type(status) != Status:
                self.logger.log_error("Setting status to something that is not a status.")
                raise Exception("Setting status to something that is not a status.")
        self.logger.log_alert(f"You are directly setting the statuses of this entity to {[status.get_name() for status in statuses]}. I hope you know what you are doing cuz this process is irreversible.")
        self.statuses = statuses

    def give_status(self, status:Status):
        self.error_if_not_in_combat()
        if type(status) != Status:
            self.logger.log_error("Invalid status.")
            raise Exception("Invalid status.")
        self.statuses.append(status)

    def take_status(self, status_name:str):
        self.error_if_not_in_combat()
        if self.get_status_by_name(status_name):
            self.statuses.remove(self.get_status_by_name(status_name))

    def get_stacks(self):
        self.error_if_not_in_combat()
        return self.stacks

    def set_stacks(self, stacks:int):
        self.error_if_not_in_combat()
        if stacks < 0 or stacks > 100:
            self.logger.log_error("Cannot set the stacks to be outside range 0-100.")
            raise Exception("Cannot set the stacks to be outside range 0-100.")
        self.logger.log_alert(f"You are directly setting the stacks of this entity to be {stacks}. I hope you know what you're doing cuz this process is irreversible.")
        self.stacks = stacks

    def give_stacks(self, stacks:int):
        self.error_if_not_in_combat()
        if self.stacks + stacks < 0:
            self.stacks = 0
            return
        if self.stacks + stacks > 100:
            self.stacks = 100
            return
        self.stacks += stacks

    def get_usable_abilities(self):
        usable = []
        for ability in self.get_abilities:
            if ability.can_use():
                usable.append(ability)
        return usable

    def get_usable_items(self):
        usable = []
        for item in self.items["active"]:
            if item.can_use():
                usable.append(item)
        return usable

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