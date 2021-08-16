import json

from utils.stats_parser import StatsParser
from rpg.players.player import Player


class Woman(Player):
    def __init__(self, name: str, user_id:str):        
        with open("res/rpg/test_stats.json", "r") as f:
            stats = StatsParser.parse_stats_range(json.load(f)["WOMAN"])
            
        super().__init__(name, user_id, stats["maxhp"], stats["str"], stats["mp"], stats["armor"], stats["mr"], stats["agility"], "karen stacks", [])