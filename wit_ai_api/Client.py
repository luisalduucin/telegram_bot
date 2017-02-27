# -*- coding: UTF-8 -*-

import os
from ResponseParser import ResponseParser
from PhraseProvider import PhraseProvider
from wit import Wit
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def menu(opcion):
	if opcion == "1":
		'''messages = []
		for messageContent in messages:
			jsonResponse = sendMessage(messageContent)
			ResponseParser(jsonResponse).prettyPrintResponse();'''
		return {"exit":False}
	elif opcion == "2":
		print("\nIngresa la petición: ")
		jsonResponse = sendMessage(raw_input())

		response = ResponseParser(jsonResponse)
		response.prettyPrintResponse();

		PhraseProvider(response).printPhrases()
		return {"response":response, "exit":False}
	else:
		return {"exit":True}

def sendMessage(messageContent):
	return client.message(messageContent)

token = os.getenv('WIT_AI_ACCESS_TOKEN', '')
client = Wit(access_token = token, actions = {})

while True:

	print("\nChatBot - Simulador\n")
	print("\t1 -> Enviar una lista predefinida de peticiones")
	print("\t2 -> Enviar una peticion")
	print("\t3 -> Salir")

	output = menu(raw_input("\nOpción: "))

	if output["exit"] == True:
		break
