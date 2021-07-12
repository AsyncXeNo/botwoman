import random

from utils.logger import Logger


class StatsParser(object):
    @staticmethod
    def parse_stats_range(stats:dict):
        maxhp = random.randint(stats["maxhp"][0], stats["maxhp"][1])
        strength = random.randint(stats["damage"]["physcial"][0], stats["damage"]["physcial"][1])
        mp = random.randint(stats["damage"]["magical"][0], stats["damage"]["magical"][1])
        armor = random.randint(stats["defense"]["physcial"][0], stats["defense"]["physcial"][1])
        mr = random.randint(stats["defense"]["magical"][0], stats["defense"]["magical"][1])
        agility = random.randint(stats["agility"][0], stats["agility"][1])

        return {"maxhp": maxhp, "str": strength, "mp": mp, "armor": armor, "mr": mr, "agility": agility/100}

    @staticmethod
    def parse_stats_normal(stats:dict):
        maxhp = stats["maxhp"]
        strength = stats["damage"]["physcial"]
        mp = stats["damage"]["magical"]
        armor = stats["defense"]["physcial"]
        mr = stats["defense"]["magical"]
        agility = stats["agility"]

        return {"maxhp": maxhp, "str": strength, "mp": mp, "armor": armor, "mr": mr, "agility": agility/100}