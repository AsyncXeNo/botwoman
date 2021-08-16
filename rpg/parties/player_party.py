from utils.my_logging import get_logger
from rpg.parties.party import Party
from rpg.players.player import Player


logger = get_logger(__name__)


class PlayerParty(Party):
    def __init__(self, owner:Player):
        super().__init__(owner)
        
        self.validate()
    
    def validate(self):
        if type(self.owner) != Player:
            logger.error("Only a player can own a player party.")
            raise Exception("Only a player can own a player party.")    

    def add_member(self, member:Player):
        if type(member) != Player:
            logger.error("Can only add players in a player party.")
            raise Exception("Can only add players in a player party.")

        self.members.append(member)