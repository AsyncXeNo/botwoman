import random


class Attack(object):
    def __init__(self, name, description, func, stacks_req=0, entity=None):
        self.entity = entity
        self.name = name
        self.description = description
        self.func = func
        self.stacks_req = stacks_req