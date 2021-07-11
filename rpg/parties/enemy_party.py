from utils.logger import Logger
from rpg.parties.party import Party
from rpg.enemies.enemy import Enemy


class EnemyParty(Party):
    def __init__(self, owner:Enemy):
        self.logger = Logger("rpg/parties/enemy_party")
        
        self.validate()
        
        super().__init__(owner)
    
    def validate(self):
        if type(self.owner) != Enemy:
            self.logger.log_error("Only an enemy can own an enemy party.")
            raise Exception("Only an enemy can own an enemy party.")    

    def add_member(self, member:Enemy):
        if type(member) != Enemy:
            self.logger.log_error("Can only add enemies in an enemy party.")
            raise Exception("Can only add enemies in an enemy party.")

        self.members.append(member)