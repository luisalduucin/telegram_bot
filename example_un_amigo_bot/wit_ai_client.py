import logging

logging.basicConfig(level=logging.INFO)

import pprint

from example_un_amigo_bot.helpers.chistes_provider import ChistesProvider
from wit_ai_api.wit_ai import WitAi

DEFAULT_RESPONSE = b'Error en el servicio de Wit.ai'
wit_ai_responses = {}
wit_ai_requests = {}
user_context = {}
chistes_provider = ChistesProvider()


class WitAiClient(object):

    def __init__(self, access_token):
        actions = {'send': WitAiClient.send, 'chiste': WitAiClient.chiste}
        self.wit_service = WitAi(access_token, actions)

    @staticmethod
    def send(request, response):
        chat_id = request.get('session_id', DEFAULT_RESPONSE)
        wit_ai_responses[chat_id] = response.get('text', DEFAULT_RESPONSE)
        wit_ai_requests[chat_id] = request.get('text', DEFAULT_RESPONSE)
        logging.info('\n\nInside send method:\n\n'
                     + '-> REQUEST:\n\n' + pprint.pformat(request) + '\n\n'
                     + '-> RESPONSE:\n\n' + pprint.pformat(response) + '\n\n'
                     + '-> WIT_AI_RESPONSES:\n\n' + pprint.pformat(wit_ai_responses) + '\n\n')

    @staticmethod
    def chiste(request):
        logging.info('\n\nInside chiste method:\n\n'
                     + '-> REQUEST:\n\n' + pprint.pformat(request)  + '\n\n')
        context = request['context']
        context['chiste'] = chistes_provider.provide()
        return context

    @staticmethod
    def get_response(chat_id):
        return wit_ai_responses.get(chat_id, DEFAULT_RESPONSE)

    @staticmethod
    def get_request(chat_id):
        return wit_ai_requests[chat_id]

    @staticmethod
    def __get_intent_value(entities):
        return entities['intent'][0]['value']

    @staticmethod
    def __get_entitie_value(entitie_name, entities):
        return entities[entitie_name][0]['value']

    def talk(self, chat_id, msg):
        if chat_id not in user_context:
            user_context[chat_id] = {}

        entities = self.wit_service.get_entities(msg)

        if 'nombre' in entities:
            user_context[chat_id]['nombre'] = WitAiClient.__get_entitie_value('nombre', entities)

        logging.info('\n\nInside talk method:\n\n'
                     + '-> Entities:\n\n' + pprint.pformat(entities) + '\n\n'
                     + '-> Context:\n\n' + pprint.pformat(user_context[chat_id]) + '\n\n')

        return self.wit_service.talk(chat_id, msg, {})
