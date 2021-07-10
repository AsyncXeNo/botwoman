from utils.logger import Logger
from utils.id_generator import IdGenerator
from rpg.entity import Entity


class Status(object):
    def __init__(self, entity:Entity, name:str, turns:int, func:function):
        self.logger = Logger("rpg/statuses/status")

        self.id = IdGenerator.generate_id()
        self.entity = entity
        self.name = name
        self.turns = turns
        self.func = func

        self.validate()
        self.logger.log_neutral(f"Created a status named {self.name} with id {self.id} which lasts for next {turns} turns.")

    def validate(self):
        if self.turns < 1:
            self.logger.log_error("Cannot create a status which lasts less than 1 turns")

    def tick(self):
        self.turns -= 1
        self.func(self.entity)
        self.check_to_destroy()

    def check_to_destroy(self):
        if self.turns < 1:
            self.destroy()

    def destroy(self):
        self.client.take_status(self)
        self.logger.log_neutral(f"Destroying status named {self.name} with id {self.id}.")