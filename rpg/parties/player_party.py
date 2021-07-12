from utils.logger import Logger
from rpg.parties.party import Party
from rpg.players.player import Player


class PlayerParty(Party):
    def __init__(self, owner:Player):
        self.logger = Logger("rpg/parties/player_party")
        
        super().__init__(owner)
        
        self.validate()
    
    def validate(self):
        if type(self.owner) != Player:
            self.logger.log_error("Only a player can own a player party.")
            raise Exception("Only a player can own a player party.")    

    def add_member(self, member:Player):
        if type(member) != Player:
            self.logger.log_error("Can only add players in a player party.")
            raise Exception("Can only add players in a player party.")

        self.members.append(member)