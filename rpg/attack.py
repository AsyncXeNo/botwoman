import random


class Attack(object):
    def __init__(self, name, description, func):
        self.name = name
        self.description = description
        self.func = func