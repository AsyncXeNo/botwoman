from utils.stats_parser import StatsParser
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


        def check(entity:Entity):
            if entity.get_stacks() < ability["check"]["stacks"]:
                return False, "not enough stacks"

            for status_name in ability["check"]["statuses"]["included"]:
                if not entity.get_status_by_name(status_name):
                    return False

            for status_name in ability["check"]["statuses"]["excluded"]:
                if entity.get_status_by_name(status_name):
                    return False

            stats = StatsParser.parse_stats_normal(ability["check"]["stats"])

            if entity.get_maxhp() < stats["maxhp"][0] or entity.get_maxhp() > stats["maxhp"][1]:
                return False
            if entity.get_str() < stats["str"][0] or entity.get_str() > stats["str"][1]:
                return False
            if entity.get_mp() < stats["mp"][0] or entity.get_mp() > stats["mp"][1]:
                return False
            if entity.get_armor() < stats["armor"][0] or entity.get_armor() > stats["armor"][1]:
                return False
            if entity.get_mr() < stats["mr"][0] or entity.get_mr() > stats["mr"][1]:
                return False
            if entity.get_agility() < stats["agility"][0] or entity.get_agility() > stats["agility"][1]:
                return False

            return True


        return Ability(name, description, entity, func, check)