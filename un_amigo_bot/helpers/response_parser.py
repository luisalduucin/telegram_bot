# -*- coding: UTF-8 -*-

import ast
import json

from .entity_type import EntityType

from un_amigo_bot.helpers.entity import Entity


class ResponseParser(object):

	def __init__(self, jsonResponse):
		self.resp_dict = ast.literal_eval(str(jsonResponse))
		self.request = self.resp_dict["_text"]
		self.entities = {}
		for key in self.resp_dict["entities"]:
			self.entities[key] = Entity(self.resp_dict["entities"][key])

	def getResponseData(self):
		return {
			EntityType.INTENT.value: self.entities[EntityType.INTENT.value],
			EntityType.TYPE_OF_PHRASE.value: self.entities[EntityType.TYPE_OF_PHRASE.value],
			EntityType.NUMBER_OF_PHRASES.value: self.entities[EntityType.NUMBER_OF_PHRASES.value]}

	def rawPrintResponse(self):
		print(json.dumps(self.resp_dict, sort_keys=True, indent=4, separators=(',', ': ')))

	def prettyPrintResponse(self):
		print("\nResponse from wit.ai:")
		print("\t-> Petición: " + self.request)
		print("\t-> Intencion: " + str(self.entities[EntityType.INTENT.value]))
		print("\t-> Tipo de frase: " + str(self.entities[EntityType.TYPE_OF_PHRASE.value]))
		print("\t-> Número de frases: " + str(self.entities[EntityType.NUMBER_OF_PHRASES.value]))
