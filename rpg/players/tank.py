import json

from utils.stats_parser import StatsParser
from utils.logger import Logger
from rpg.players.player import Player


class Tank(Player):
    def __init__(self, name: str, user_id:str):
        self.logger = Logger("rpg/players/tank")
        
        with open("res/rpg/test_stats.json", "r") as f:
            stats = StatsParser.parse_stats_range(json.load(f)["TANK"])
            
        super().__init__(name, user_id, stats["maxhp"], stats["str"], stats["mp"], stats["armor"], stats["mr"], stats["agility"], "resolve", [])