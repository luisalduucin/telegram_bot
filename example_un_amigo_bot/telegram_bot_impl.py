from example_un_amigo_bot.helpers.custom_keyboard_provider import CustomKeyboardProvider
from example_un_amigo_bot.helpers.questions_provider import QuestionsProvider
from telegram_api.telegram_bot import TelegramBot
from .wit_ai_client import WitAiClient

START_QUESTIONARY_SIGNAL = 'me gustaría conocerte, como te describes a ti mismo?'


class TelegramBotImpl(TelegramBot):
    def __init__(self, bot_name, access_token, wit_ai_access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)
        self.wit_client = WitAiClient(wit_ai_access_token)
        self.questions_repository = QuestionsProvider()
        self.custom_keyboard_repository = CustomKeyboardProvider()
        self.current_question = {}

    def get_question_with_custom_keyboard(self, chat_id):
        question_index = self.current_question[chat_id]
        question = self.questions_repository.provide(question_index)
        custom_keyboard = self.custom_keyboard_repository.provide(question)
        return question, custom_keyboard

    def send_wit_ai_response(self, chat_id, message='Retomar conversacion libre'):
        self.wit_client.talk(chat_id, message)
        self.send(chat_id, self.wit_client.get_response(chat_id))

    def handler(self, msg):
        content_type, chat_type, chat_id = TelegramBot.glance(msg)
        message = msg['text']

        if content_type == 'text':

            if chat_id not in self.current_question and START_QUESTIONARY_SIGNAL in self.wit_client.get_response(chat_id).decode('utf-8'):
                # TODO guardar como se describe a si mismo
                self.current_question[chat_id] = 0
                self.send_current_question(chat_id)
            elif chat_id in self.current_question:
                self.current_question[chat_id] += 1
                if self.questions_repository.are_remaining_questions(self.current_question[chat_id]):
                    self.send_current_question(chat_id)
                else:
                    self.current_question.pop(chat_id, None)
                    self.send_wit_ai_response(chat_id)
            else:
                self.send_wit_ai_response(chat_id, message)

        else:
            self.send(chat_id, 'Ese tipo de message no es valido')

    def send_current_question(self, chat_id):
        question, custom_keyboard = self.get_question_with_custom_keyboard(chat_id)
        self.send_with_custom_keyboard(chat_id, question, custom_keyboard)
