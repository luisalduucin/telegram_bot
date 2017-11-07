import json
import os

from random import randrange


class ResourceProvider:

    MAX_RESOURCES_ALLOWED = 5

    def __init__(self):
        resources_file = open(os.path.dirname(__file__) + '/../data/resources.json', encoding='utf-8')
        self.resources_repository = json.load(resources_file)['resources']
        resources_file.close()

    def provide(self):
        resources_to_send = randrange(1, self.MAX_RESOURCES_ALLOWED, 1)
        resources = []
        for x in range(0, resources_to_send):
            resource = self.resources_repository[randrange(0, len(self.resources_repository), 1)]
            while resource in resources:
                resource = self.resources_repository[randrange(0, len(self.resources_repository), 1)]
            resources.append(resource)
        return resources
