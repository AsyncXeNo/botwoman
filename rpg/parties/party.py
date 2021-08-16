from utils.my_logging import get_logger
from utils.id_generator import IdGenerator
from rpg.entity import Entity


logger = get_logger(__name__)


class Party(object):
    def __init__(self, owner:Entity):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        self.owner = owner

        self.members = [self.owner]
        
        logger.debug(f"Created a party with id {self.ID}.")

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

        logger.warn(f"Member with id {member_id} not found in members.")