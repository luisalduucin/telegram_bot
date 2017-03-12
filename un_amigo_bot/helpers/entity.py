
class Entity(object):
    def __init__(self, content):
        self.attributes = content[0]

    def get_value(self):
        return self.attributes["value"]

    def get_confidence(self):
        return self.attributes["confidence"]

    def __str__(self):
        return "Valor: " + str(self.get_value()) + " Certeza: " + str(self.get_confidence())
