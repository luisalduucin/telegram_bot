import logging
import pprint

from example_un_amigo_bot.helpers.custom_keyboard_provider import CustomKeyboardProvider
from example_un_amigo_bot.helpers.questions_provider import QuestionsProvider
from telegram_api.telegram_bot import TelegramBot
from .wit_ai_client import WitAiClient

SELF_DESCRIPTION_TAG = 'SELF_DESCRIPTION'

DEPRESSION_SCORE_TAG = 'DEPRESSION_SCORE'

START_QUESTIONARY_SIGNAL = 'me gustaría conocerte, como te describes a ti mismo?'


class TelegramBotImpl(TelegramBot):
    def __init__(self, bot_name, access_token, wit_ai_access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)
        self.wit_client = WitAiClient(wit_ai_access_token)
        self.questions_repository = QuestionsProvider()
        self.custom_keyboard_repository = CustomKeyboardProvider()
        self.current_question_index = {}
        self.depression_profile = {}

    def get_question_with_custom_keyboard(self, chat_id):
        question_index = self.current_question_index[chat_id]
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
            if message == '/start':
                self.send_wit_ai_response(chat_id, 'Hola')
            elif message == '/report':
                self.send_statistics()
            else:
                if chat_id not in self.current_question_index and \
                                START_QUESTIONARY_SIGNAL in self.wit_client.get_response(chat_id).decode('utf-8'):
                    self.save_self_description(chat_id, message)
                    self.current_question_index[chat_id] = 0
                    self.send_current_question(chat_id)
                elif chat_id in self.current_question_index:
                    self.current_question_index[chat_id] += 1
                    if self.questions_repository.are_remaining_questions(self.current_question_index[chat_id]):
                        self.send_current_question(chat_id)
                        self.update_depression_score(chat_id, response=message)
                    else:
                        self.current_question_index.pop(chat_id, None)
                        self.send_wit_ai_response(chat_id)
                else:
                    self.send_wit_ai_response(chat_id, message)

        else:
            self.send(chat_id, 'Ese tipo de message no es valido')

    def send_current_question(self, chat_id):
        question, custom_keyboard = self.get_question_with_custom_keyboard(chat_id)
        self.send_with_custom_keyboard(chat_id, question, custom_keyboard)

    def save_self_description(self, chat_id, description):
        if chat_id not in self.depression_profile:
            self.depression_profile[chat_id] = {}
        self.depression_profile[chat_id][SELF_DESCRIPTION_TAG] = description
    
    def update_depression_score(self, chat_id, response):
        previous_question_index = self.current_question_index[chat_id] - 1
        question = self.questions_repository.provide(previous_question_index)
        button_value = self.custom_keyboard_repository.get_button_value(question, response)
        if chat_id not in self.depression_profile:
            self.depression_profile[chat_id] = {}
        if DEPRESSION_SCORE_TAG not in self.depression_profile[chat_id]:
            self.depression_profile[chat_id][DEPRESSION_SCORE_TAG] = 0
        self.depression_profile[chat_id][DEPRESSION_SCORE_TAG] += int(button_value)

    def send_statistics(self):
        logging.info('\n\nUsers Statistics:\n\n'
                     + '-> User Profiles:\n\n' + pprint.pformat(self.depression_profile) + '\n\n')
