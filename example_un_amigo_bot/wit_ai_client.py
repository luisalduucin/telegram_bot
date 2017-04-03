from wit_ai_api.wit_ai import WitAi
from example_un_amigo_bot.helpers.response_parser import ResponseParser
from example_un_amigo_bot.helpers.phrase_provider import PhraseProvider

DEFAULT_RESPONSE = 'Error en el servicio de Wit.ai'
user_response = ['NOPE']


class WitAiClient(object):

    user_context = {}

    def __init__(self, access_token):
        actions = {'send': WitAiClient.send}
        self.wit_service = WitAi(access_token, actions)

    @staticmethod
    def send(request, response):
        user_response[0] = response.get('text', DEFAULT_RESPONSE)

    def talk(self, chat_id, msg):
        if chat_id not in self.user_context:
            self.user_context[chat_id] = {}

        entities = self.wit_service.get_entities(msg)
        print(entities)

        if 'intent' in entities:
            if entities['intent'][0]['value'] == 'recomendar_frase':
                response = ResponseParser(self.wit_service.analyze(msg))
                response.prettyPrintResponse()
                self.user_context[chat_id]['frases'] = str(PhraseProvider(response).provide())

        if 'tipo_dia' in entities:
            self.user_context[chat_id]['tipo_dia'] = entities['tipo_dia'][0]['value']
            provider = PhraseProvider()
            provider.set_quantity(1)
            provider.set_type_of_phrase('motivacional')
            self.user_context[chat_id]['frases'] = str(provider.provide())

        print("Context: " + str(self.user_context[chat_id]))
        return self.wit_service.talk(chat_id, msg, self.user_context[chat_id])
