from utils.logger import Logger
from rpg.parties.player_party import PlayerParty
from rpg.parties.enemy_party import EnemyParty
from rpg.turn import Turn


class Battle(object):
    def __init__(self, players:PlayerParty, enemies:EnemyParty):
        self.logger = Logger("rpg/battle")


        self.players = players
        self.enemies = enemies

        self.logger.log_neutral(f"Starting a battle between {self.players.get_owner().get_name()}'s party and {self.enemies.get_owner().get_name()}'s party")

        self.ready_for_battle()
        self.start_battle()

    def ready_for_battle(self):
        self.ready_players()
        self.ready_enemies()

    def ready_players(self):
        for player in self.players.get_members():
            player.ready_for_battle(self)
    
    def ready_enemies(self):
        for enemy in self.enemies.get_members():
            enemy.ready_for_battle(self)

    def start_battle(self):
        while not self.check_if_end():
            Turn(self)

        # conclude battle

    def check_if_end(self):
        return self.check_if_players_dead() or self.check_if_enemies_dead()

    def check_if_players_dead(self):
        for player in self.players.get_members():
            if player.get_hp() > 0:
                return False
        return True

    def check_if_enemies_dead(self):
        for enemy in self.enemies.get_members():
            if enemy.get_hp() > 0:
                return False
        return True