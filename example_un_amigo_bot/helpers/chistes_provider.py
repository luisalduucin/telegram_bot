import json
import os

from random import randrange


class ChistesProvider:
    def __init__(self):
        chistes_file = open(os.path.dirname(__file__) + '/../data/chistes.json', encoding='utf-8')
        self.chistes = json.load(chistes_file)
        chistes_file.close()

    def provide(self):
        return self.chistes["chiste_" + str(randrange(1, len(self.chistes), 1))]
