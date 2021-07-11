from utils.logger import Logger
from utils.id_generator import IdGenerator
from rpg.entity import Entity


class Party(object):
    def __init__(self, owner:Entity):
        self.logger = Logger("rpg/parties/party")
        
        self.id = IdGenerator.generate_id()
        self.owner = owner

        self.members = [self.owner]
        
        self.logger.log_neutral(f"Created a party with id {self.id}.")

    def get_id(self):
        return self.id

    def get_owner(self):
        return self.owner

    def get_members(self):
        return self.members

    def remove_member(self, member_id:str):
        self.members.remove(self.get_member_by_id(member_id)) 
    
    # helper

    def get_member_by_id(self, member_id:str):
        for member in self.members:
            if member.get_id() == member_id:
                return member

        self.logger.log_alert(f"Member with id {member_id} not found in members.")