from telegram_api.telegram_bot import TelegramBot
from .wit_ai_client import WitAiClient
from .wit_ai_client import user_response


class TelegramBotImpl(TelegramBot):

    active_users = {}

    def __init__(self, bot_name, access_token, wit_ai_access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)
        self.wit_client = WitAiClient(wit_ai_access_token)

    def set_operation_mode(self, operation_mode, chat_id):

        if operation_mode.startswith('/') and operation_mode != '/change_mode':
            self.active_users[chat_id] = {'operationMode': operation_mode}

            if operation_mode == '/witai_mode':
                self.bot.sendMessage(chat_id, 'Modo de operacion ' + operation_mode + ' activado')
        else:
            self.bot.sendMessage(chat_id, 'Selecciona un modo de operacion')

    def handler(self, msg):
        content_type, chat_type, chat_id = TelegramBot.glance(msg)
        message = msg['text']

        user = self.active_users.get(chat_id, None)

        if content_type == 'text':

            if not user:
                self.set_operation_mode(message, chat_id)
            else:
                if msg['text'] == '/change_mode':

                    self.active_users.pop(chat_id, None)
                    self.set_operation_mode(message, chat_id)

                elif user['operationMode'] == '/echo_mode':

                    self.bot.sendMessage(chat_id, message)

                elif user['operationMode'] == '/debug_mode':

                    print(content_type, chat_type, chat_id)

                elif user['operationMode'] == '/witai_mode':

                    self.wit_client.talk(chat_id, msg['text'])
                    self.bot.sendMessage(chat_id, user_response[0])

                else:

                    self.bot.sendMessage(chat_id, 'Ese modo de operacion no es valido')
        else:
            self.bot.sendMessage(chat_id, 'Ese tipo de message no es valido')
