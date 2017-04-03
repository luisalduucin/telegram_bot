from telegram_api.telegram_bot import TelegramBot
from .wit_ai_client import WitAiClient
from .wit_ai_client import user_response


class TelegramBotImpl(TelegramBot):
    def __init__(self, bot_name, access_token, wit_ai_access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)
        self.wit_client = WitAiClient(wit_ai_access_token)

    def handler(self, msg):
        content_type, chat_type, chat_id = TelegramBot.glance(msg)
        message = msg['text']

        if content_type == 'text':
            self.wit_client.talk(chat_id, message)
            self.bot.sendMessage(chat_id, user_response[0])
        else:
            self.bot.sendMessage(chat_id, 'Ese tipo de message no es valido')
