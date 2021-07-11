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
                target.give_hp(item["func"]["hp"])
                target.give_agility(item["func"]["agility"])
                target.give_str(item["func"]["damage"]["physical"])
                target.give_mp(item["func"]["damage"]["magical"])
                target.give_armor(item["func"]["defense"]["physical"])
                target.give_mr(item["func"]["defense"]["magical"])
                target.deal_physical(item["func"]["deal"]["physical"])
                entity.deal_magical(item["func"]["deal"]["magical"])
                entity.give_status(StatusesParser.parse_status(item["func"]["status"]))
                return item["func_dialogue"]

        
        return ActiveItem(name, description, level, func)

    @staticmethod
    def parse_passive(item:dict):
        name = item["name"]
        description = item["description"]
        level = item["level"]

        stats = StatsParser.parse_stats(item["stats"])

        maxhp = stats["maxhp"]
        strength = stats["str"]
        mp = stats["mp"]
        armor = stats["armor"]
        mr = stats["mr"]
        agility = stats["agility"]

        return PassiveItem(name, description, level, maxhp, strength, mp, armor, mr, agility)
