import random

from utils.logger import Logger


class StatsParser(object):
    @staticmethod
    def parse_stats_range(stats:dict):
        maxhp = random.randint(stats["maxhp"])
        strength = random.randint(stats["damage"]["physcial"])
        mp = random.randint(stats["damage"]["magical"])
        armor = random.randint(stats["defense"]["physcial"])
        mr = random.randint(stats["defense"]["magical"])
        agility = random.randint(stats["agility"])

        return {"maxhp": maxhp, "str": strength, "mp": mp, "armor": armor, "mr": mr, "agility": agility}

    @staticmethod
    def parse_stats_normal(stats:dict):
        maxhp = stats["maxhp"]
        strength = stats["damage"]["physcial"]
        mp = stats["damage"]["magical"]
        armor = stats["defense"]["physcial"]
        mr = stats["defense"]["magical"]
        agility = stats["agility"]

        return {"maxhp": maxhp, "str": strength, "mp": mp, "armor": armor, "mr": mr, "agility": agility}