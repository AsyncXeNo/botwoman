from utils.logger import Logger
from utils.id_generator import IdGenerator


class Item(object):
    def __init__(self, name:str, description:str, level:int):
        self.logger = Logger("rpg/items/item")

        self.id = IdGenerator.generate_id()
        self.name = name
        self.description = description
        self.level = level

        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_id(self):
        return self.id

    def get_level(self):
        return self.level