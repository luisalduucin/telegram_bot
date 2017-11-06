import json
import os

from random import randrange


class JokesProvider:
    def __init__(self):
        jokes_file = open(os.path.dirname(__file__) + '/../data/jokes.json', encoding='utf-8')
        self.jokes = json.load(jokes_file)
        jokes_file.close()

    def provide(self):
        return self.jokes["joke_" + str(randrange(1, len(self.jokes), 1))]
