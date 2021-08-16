from utils.my_logging import get_logger
from rpg.parties.party import Party
from rpg.enemies.enemy import Enemy


logger = get_logger(__name__)


class EnemyParty(Party):
    def __init__(self, owner:Enemy):
        self.validate()
        
        super().__init__(owner)
    
    def validate(self):
        if type(self.owner) != Enemy:
            logger.error("Only an enemy can own an enemy party.")
            raise Exception("Only an enemy can own an enemy party.")    

    def add_member(self, member:Enemy):
        if type(member) != Enemy:
            logger.error("Can only add enemies in an enemy party.")
            raise Exception("Can only add enemies in an enemy party.")

        self.members.append(member)