import copy
from rpg.turn import Turn


class Battle_Manager(object):
    def __init__(self, room):
        self.room = room
        self.ability_effects = [
            {
                "name": "poison",
                "turns": 0,
                "affects": [copy.copy(self.room.client.get_cog("RPG").get_party_by_owner_id(650999961214779392))], # list of everyone it affects
                "effects": {
                    "health": 100,
                    "physcial damage": 1331,
                    "magic damage": 1276,
                    "physcial buff": 1234,
                    "magic buff": -2156,
                    "physcial defense": -113,
                    "magic defense": 123,
                    "agility": 0.5
                }
            }
        ]

        self.battles = {}

    def clean_up(self):
        for effect in self.ability_effects:
            if effect["turns"] == 0:
                self.ability_effects.remove(effect)

    def start_battle(self, index):
        player_party = copy.copy(self.room.parties[index])
        enemy_party = self.room.enemyparties[index]

        self.battles[player_party[0]] = {
            "players": player_party,
            "enemies": enemy_party,
            "ability_effects": [
                {
                    "name": "poison",
                    "turns": 0,
                    "affects": [copy.copy(self.room.client.get_cog("RPG").get_party_by_owner_id(650999961214779392))], # list of everyone it affects
                    "effects": {
                        "health": 100,
                        "physcial damage": 1331,
                        "magic damage": 1276,
                        "physcial buff": 1234,
                        "magic buff": -2156,
                        "physcial defense": -113,
                        "magic defense": 123,
                        "agility": 0.5
                    }
                }
            ]
        }

        while not self.check_if_event_over(player_party, enemy_party):
            abilities = {}
            self.clean_up()

            for player in player_party:
                abilities[player] = self.room.client.get_cog("RPG_GAME").prompt_player_for_attack(player)
                if not abilities[player]:
                    raise Exception("Player did not return an attack, which should not be possible.")

            for enemy in enemy_party:
                abilities[enemy] = enemy.get_random_attack()
                if not abilities[enemy]:
                    raise Exception("Enemy did not return an attack, which should not be possible.")

            Turn(self).start_turn(abilities, player_party, enemy_party)

        # event ending formalities idk

    def check_if_event_over(self, player_party, enemy_party):
        players_alive = False
        enemies_alive = False

        for player in player_party:
            if player.hp > 0:
                players_alive = True
        for enemy in enemy_party:
            if enemy.hp > 0:
                enemies_alive = True

        return (not players_alive) or (not enemies_alive)
