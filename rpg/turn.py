
class Turn(object):
    def __init__(self, battle_manager):
        self.battle_manager = battle_manager

    def start_turn(self, abilities):
        self.handle_effects()
        for player in battle_manager.player_party:
            abilities[player](self.battle_manager.room.ctx, )

        for enemy in battle_manager.enemy_party:
            abilities[enemy]()

    def handle_effects(self):
        for effect in self.battle_manager.ability_effects:
            effect["turns"] -= 1
