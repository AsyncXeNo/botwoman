from rpg.ability import Ability
from utils.statuses_parser import StatusesParser
from rpg.battle import Battle
from rpg.entity import Entity
from utils.logger import Logger


class AbilitiesParser(object):
    @staticmethod
    def parse_ability(ability:dict, entity:Entity):
        name = ability["name"]
        description = ability["description"]


        def func(entity:Entity, battle:Battle):
            targets = None
            if ability["func"]["target"] == "players":
                targets = battle.get_player_party().get_members()
            elif ability["func"]["target"] == "enemies":
                targets = battle.get_enemy_party().get_members()

            if targets:
                if ability["func"]["single_target"]:
                    targets = [entity.get_target(targets)]

            for target in targets:
                target.give_hp(ability["func"]["hp"])
                target.give_agility(ability["func"]["agility"])
                target.give_str(ability["func"]["damage"]["physical"])
                target.give_mp(ability["func"]["damage"]["magical"])
                target.give_armor(ability["func"]["defense"]["physical"])
                target.give_mr(ability["func"]["defense"]["magical"])
                target.deal_physical(ability["func"]["deal"]["physical"])
                entity.deal_magical(ability["func"]["deal"]["magical"])
                entity.give_status(StatusesParser.parse_status(ability["func"]["status"]))
                return ability["func"]["dialogue"]


        return Ability(name, description, entity, func)