from telegram_api.telegram_bot import TelegramBot


class TelegramBotImpl(TelegramBot):
    def __init__(self, bot_name, access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)

    def handler(self, msg):
        content_type, chat_type, chat_id = TelegramBot.glance(msg)
        message = msg['text']

        if content_type == 'text':
            self.bot.sendMessage(chat_id, message)
        else:
            self.bot.sendMessage(chat_id, 'Ese tipo de message no es valido')
