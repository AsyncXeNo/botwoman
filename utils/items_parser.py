from rpg.items.passive_item import PassiveItem
from utils.stats_parser import StatsParser
from rpg.items.active_item import ActiveItem
from utils.statuses_parser import StatusesParser
from rpg.battle import Battle
from rpg.entity import Entity
from utils.logger import Logger


class ItemsParser(object):
    @staticmethod
    def parse_active(item:dict):
        name = item["name"]
        description = item["description"]
        level = item["level"]


        def func(entity:Entity, battle:Battle):
            targets = None
            if item["func"]["target"] == "players":
                targets = battle.get_player_party().get_members()
            elif item["func"]["target"] == "enemies":
                targets = battle.get_enemy_party().get_members()

            if targets:
                if item["func"]["single_target"]:
                    targets = [entity.get_target(targets)]

            for target in targets:
                target.set_hp(item["func"]["set"]["hp"])
                target.set_agility(item["func"]["set"]["agility"])
                target.set_str(item["func"]["set"]["damage"]["physical"])
                target.set_mp(item["func"]["set"]["damage"]["magical"])
                target.set_armor(item["func"]["set"]["defense"]["physical"])
                target.set_mr(item["func"]["set"]["defense"]["magical"])
                target.set_status(StatusesParser.parse_status(item["func"]["set"]["status"]))

                target.give_hp(item["func"]["give"]["hp"])
                target.give_agility(item["func"]["give"]["agility"])
                target.give_str(item["func"]["give"]["damage"]["physical"])
                target.give_mp(item["func"]["give"]["damage"]["magical"])
                target.give_armor(item["func"]["give"]["defense"]["physical"])
                target.give_mr(item["func"]["give"]["defense"]["magical"])
                target.give_status(StatusesParser.parse_status(item["func"]["give"]["status"]))

                target.deal_physical(item["func"]["deal"]["physical"])
                target.deal_magical(item["func"]["deal"]["magical"])
                
                return item["func_dialogue"]

        
        return ActiveItem(name, description, level, func)

    @staticmethod
    def parse_passive(item:dict):
        name = item["name"]
        description = item["description"]
        level = item["level"]

        stats = StatsParser.parse_stats_normal(item["stats"])

        maxhp = stats["maxhp"]
        strength = stats["str"]
        mp = stats["mp"]
        armor = stats["armor"]
        mr = stats["mr"]
        agility = stats["agility"]

        return PassiveItem(name, description, level, maxhp, strength, mp, armor, mr, agility)
