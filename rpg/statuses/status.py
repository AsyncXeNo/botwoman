from utils.my_logging import get_logger
from utils.id_generator import IdGenerator


logger = get_logger(__name__)


class Status(object):
    def __init__(self, name:str, turns:int, bad:bool, func, end_func):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        self.name = name
        self.turns = turns
        self.bad = bad
        self.func = func
        self.end_func = end_func

        self.entity = None

        self.validate()
        self.logger.log_neutral(f"Created a status named {self.name} with id {self.id} which lasts for next {turns} turns.")
    
    def is_bad(self):
        return self.bad    

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_turns(self):
        return self.turns

    def set_turns(self, turns:int):
        self.turns = turns


    def give_turns(self, turns:int):
        self.turns += turns

    def get_entity(self):
        return self.entity
        
    def set_entity(self, entity):
        self.entity = entity   

    def validate(self):
        if self.turns < 1:
            self.logger.log_error("Cannot create a status which lasts less than 1 turns")

    def tick(self):
        if self.entity:
            self.check_to_destroy()
            self.turns -= 1
            self.func(self.entity)

    def check_to_destroy(self):
        if self.turns < 1:
            if self.end_func:
                self.end_func(self.entity)
            self.destroy()

    def destroy(self):
        self.entity.take_status(self.id)
        self.logger.log_neutral(f"Destroying status named {self.name} with id {self.id}.")