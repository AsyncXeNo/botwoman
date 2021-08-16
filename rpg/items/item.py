from utils.my_logging import get_logger
from utils.id_generator import IdGenerator


logger = get_logger(__name__)


class Item(object):
    def __init__(self, name:str, description:str, level:int):
        self.ID = f'{self.__class__.__name__}-{IdGenerator.generate_id()}'
        self.name = name
        self.description = description
        self.level = level

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_id(self):
        return self.id

    def get_level(self):
        return self.level