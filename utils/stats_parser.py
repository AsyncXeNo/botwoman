import random

from utils.logger import Logger


class StatsParser(object):
    @staticmethod
    def parse_stats(stats:dict):
        maxhp = random.randint(stats["maxhp"])
        strength = random.randint(stats["damage"]["physcial"])
        mp = random.randint(stats["damage"]["magical"])
        armor = random.randint(stats["defense"]["physcial"])
        mr = random.randint(stats["defense"]["magical"])
        agility = random.randint(stats["agility"])

        return {"maxhp": maxhp, "str": strength, "mp": mp, "armor": armor, "mr": mr, "agility": agility}