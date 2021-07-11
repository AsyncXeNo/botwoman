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
                target.set_hp(ability["func"]["set"]["hp"])
                target.set_agility(ability["func"]["set"]["agility"])
                target.set_str(ability["func"]["set"]["damage"]["physical"])
                target.set_mp(ability["func"]["set"]["damage"]["magical"])
                target.set_armor(ability["func"]["set"]["defense"]["physical"])
                target.set_mr(ability["func"]["set"]["defense"]["magical"])
                target.set_status(StatusesParser.parse_status(ability["func"]["set"]["status"]))

                target.give_hp(ability["func"]["give"]["hp"])
                target.give_agility(ability["func"]["give"]["agility"])
                target.give_str(ability["func"]["give"]["damage"]["physical"])
                target.give_mp(ability["func"]["give"]["damage"]["magical"])
                target.give_armor(ability["func"]["give"]["defense"]["physical"])
                target.give_mr(ability["func"]["give"]["defense"]["magical"])
                target.give_status(StatusesParser.parse_status(ability["func"]["give"]["status"]))

                target.deal_physical(ability["func"]["deal"]["physical"])
                target.deal_magical(ability["func"]["deal"]["magical"])
                
                return ability["func"]["give"]["dialogue"]


        return Ability(name, description, entity, func)