import string
import random
import json

from utils.logger import Logger


class IdGenerator(object):
    fileopen = False

    @staticmethod
    def generate_id(length:int=8):
        while True:
            if not IdGenerator.fileopen:       
                IdGenerator.fileopen = True
                with open("data/generated_ids.json", "r") as f:
                    generated = json.load(f)

                gen = "".join(random.choices(string.ascii_uppercase, k=length))
                while gen in generated:
                    gen = ''.join(random.choices(string.ascii_uppercase, k=length))
                generated.append(gen)
                
                with open("data/generated_ids.json", "w") as f:
                    json.dump(generated, f, indent=4)
                IdGenerator.fileopen = False
                return gen