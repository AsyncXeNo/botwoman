from utils.id_generator import IdGenerator
from utils.my_logging import get_logger
from rpg.turn import Turn


logger = get_logger(__name__)


class Battle(object):
    def __init__(self, application, players, enemies):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        self.application = application
        self.players = players
        self.enemies = enemies

        logger.info(f"Starting a battle between {self.players.get_owner().get_name()}'s party and {self.enemies.get_owner().get_name()}'s party.")

        self.ready_for_battle()
        self.start_battle()

    def get_id(self):
        return self.id

    def get_player_party(self):
        return self.players

    def get_enemy_party(self):
        return self.enemies

    def ready_for_battle(self):
        self.ready_players()
        self.ready_enemies()

    def ready_players(self):
        for player in self.players.get_members():
            player.ready_for_battle(self)
    
    def ready_enemies(self):
        for enemy in self.enemies.get_members():
            enemy.ready_for_battle(self)

    def end_for_players(self):
        for player in self.players.get_members():
            player.end_battle()

    def end_for_enemies(self):
        for enemy in self.enemies.get_members():
            enemy.end_battle()

    def start_battle(self):
        count = 0
        while not self.check_if_end():
            count += 1
            Turn(self, count)

        self.end_battle()
        # conclude battle
        #

    def end_battle(self):
        self.end_for_players()
        self.end_for_enemies()

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