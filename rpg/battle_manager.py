import copy
from rpg.turn import Turn


class Battle_Manager(object):
    def __init__(self, room):
        self.room = room
        self.battles = {}

    def clean_up(self, player_token):
        for effect in self.battles[player_token]["ability_effects"]:
            if effect["turns"] == 0:
                self.battles[player_token]["ability_effects"].remove(effect)

    async def start_battle(self, index):
        player_party = copy.copy(self.room.parties[index])
        enemy_party = self.room.enemy_parties[index]

        self.battles[player_party[0]] = {
            "players": player_party,
            "enemies": enemy_party,
            "ability_effects": []
        }

        turn = 0
        while not self.check_if_event_over(player_party, enemy_party):
            turn += 1
            await self.room.ctx.send(f"Turn {turn}")
            abilities = {}
            self.clean_up(player_party[0])

            for player in player_party:
                abilities[player] = await self.room.client.get_cog("RPG_GAME").prompt_player_for_attack(self.room.ctx, player)
                if not abilities[player]:
                    raise Exception("Player did not return an attack, which should not be possible.")
            
            for enemy in enemy_party:
                abilities[enemy] = enemy.get_random_attack()
                if not abilities[enemy]:
                    raise Exception("Enemy did not return an attack, which should not be possible.")

            await Turn(self).start_turn(abilities, player_party, enemy_party)

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
