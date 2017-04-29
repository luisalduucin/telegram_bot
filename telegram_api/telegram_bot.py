from abc import ABCMeta, abstractmethod
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup


class TelegramBot(object):
    __metaclass__ = ABCMeta

    def __init__(self, bot_name, access_token):
        self.bot_name = bot_name
        self.bot = telepot.Bot(access_token)

    def send(self, chat_id, msg):
        self.bot.sendMessage(chat_id, msg)

    def send_with_custom_keyboard(self, chat_id, msg, custom_keyboard):
        self.bot.sendMessage(chat_id, msg, reply_markup=ReplyKeyboardMarkup(keyboard=[custom_keyboard]))

    @staticmethod
    def glance(msg):
        return telepot.glance(msg)

    @abstractmethod
    def handler(self, msg):
        raise NotImplementedError()

    def start(self):
        self.bot.message_loop(self.handler)
        print(self.bot_name + ' is set up and listening ...')
        while True:
            time.sleep(10)
