from utils.logger import Logger
from utils.math import Vector2


class Room(object):
    def __init__(self, pos:Vector2):
        self.logger = Logger("rpg/room")
        
        self.pos = pos