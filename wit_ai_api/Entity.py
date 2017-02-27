class Entity(object):

	def __init__(self, content):
		self.attributes = content[0]

	def getValue(self):
		return self.attributes["value"]

	def getConfidence(self):
		return self.attributes["confidence"]

	def __str__(self):
		return  "Valor: " + str(self.getValue()) +  " Certeza: " + str(self.getConfidence())
