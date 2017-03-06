import os
import uuid
from WitAPI import WitAPI

from wit_ai_api.ResponseParser import ResponseParser
from wit_ai_api.PhraseProvider import PhraseProvider

class InteractiveWitClient(object):

	def __init__(self, access_token, actions):
		
		self.witService = WitAPI(access_token, actions)
		self.session_id = uuid.uuid4()
		self.context = {}

	def talk(self, msg):

		entities = self.witService.getEntities(msg)
		print(entities)

		if 'intent' in entities:
			if entities['intent'][0]['value'] == 'recomendar_frase':
				response = ResponseParser(self.witService.analyze(msg))
				response.prettyPrintResponse();
				self.context['frases'] = str(PhraseProvider(response).provide())

		if 'tipo_dia' in entities:
			self.context['tipo_dia'] = entities['tipo_dia'][0]['value']
			provider = PhraseProvider()
			provider.setQuantity(1)
			provider.setTypeOfPhrase('motivacional')
			self.context['frases'] = str(provider.provide())

		print("Context: " + str(self.context))
		return self.witService.talk(self.session_id, msg, self.context)
