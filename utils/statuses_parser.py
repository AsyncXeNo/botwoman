from utils.logger import Logger
from rpg.statuses.status import Status
from rpg.entity import Entity


class StatusesParser(object):
    @staticmethod
    def parse_status(status:dict):
        name = status["name"]
        turns = status["turns"]
        bad = status["bad"]


        def func(entity:Entity):
            entity.give_hp(status["func"]["hp"])
            entity.give_agility(status["func"]["agility"])
            entity.give_str(status["func"]["damage"]["physical"])
            entity.give_mp(status["func"]["damage"]["magical"])
            entity.give_armor(status["func"]["defense"]["physical"])
            entity.give_mr(status["func"]["defense"]["magical"])
            entity.deal_physical(status["func"]["deal"]["physical"])
            entity.deal_magical(status["func"]["deal"]["magical"])
            return status["func"]["dialogue"]


        if status["end_func"]:
            def end_func(entity:Entity):
                entity.give_hp(status["end_func"]["hp"])
                entity.give_agility(status["end_func"]["agility"])
                entity.give_str(status["end_func"]["damage"]["physical"])
                entity.give_mp(status["end_func"]["damage"]["magical"])
                entity.give_armor(status["end_func"]["defense"]["physical"])
                entity.give_mr(status["end_func"]["defense"]["magical"])
                entity.deal_physical(status["end_func"]["deal"]["physical"])
                entity.deal_magical(status["end_func"]["deal"]["magical"])
                entity.give_status(StatusesParser.parse_status(status["end_func"]["status"]))
                return status["end_func"]["dialogue"]
            
        else:
            end_func = None

        return Status(name, turns, bad, func, end_func)