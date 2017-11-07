# coding=utf-8
import logging
import pprint
from string import Template

from example_un_amigo_bot.providers.custom_keyboard_provider import CustomKeyboardProvider
from example_un_amigo_bot.providers.questions_provider import QuestionsProvider
from example_un_amigo_bot.providers.resource_provider import ResourceProvider
from telegram_api.telegram_bot import TelegramBot
from .wit_ai_client import WitAiClient

SELF_DESCRIPTION_TAG = 'SELF_DESCRIPTION'

DEPRESSION_SCORE_TAG = 'DEPRESSION_SCORE'
DEPRESSION_CLASSIFICATION_TAG = 'DEPRESSION_CLASSIFICATION'

NO_DEPRESSION_TAG = 'No depresion'
MODERATED_DEPRESSION_TAG = 'Depresion moderada'
ESTABLISHED_DEPRESSION_TAG = 'Depresion establecida'

START_QUESTIONARY_SIGNAL = 'me gustaría conocerte, como te describes a ti mismo?'
FINISH_QUESTIONARY_SIGNAL = 'Muchisimas gracias por responder a todas mis preguntas'

VIDEO_MESSAGE_TEMPLATE = Template('$title \n $url')
COMPOUND_VIDEO_MESSAGE_TEMPLATE = Template('$title \n $url \n $description')


def calculate_depression_class(depression_score):
    if 0 <= depression_score <= 17:
        return NO_DEPRESSION_TAG
    elif 18 <= depression_score <= 22:
        return MODERATED_DEPRESSION_TAG
    else:
        return ESTABLISHED_DEPRESSION_TAG


class TelegramBotImpl(TelegramBot):
    def __init__(self, bot_name, access_token, wit_ai_access_token):
        super(TelegramBotImpl, self).__init__(bot_name, access_token)
        self.wit_client = WitAiClient(wit_ai_access_token)
        self.questions_repository = QuestionsProvider()
        self.resources_repository = ResourceProvider()
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
                elif chat_id not in self.current_question_index and \
                        FINISH_QUESTIONARY_SIGNAL in self.wit_client.get_response(chat_id).decode('utf-8'):
                    if NO_DEPRESSION_TAG != self.depression_profile[chat_id][DEPRESSION_CLASSIFICATION_TAG]:
                        self.send_resources(chat_id)
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
            self.send(chat_id, 'Ese tipo de mensaje no es valido')

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
        depression_score = self.depression_profile[chat_id][DEPRESSION_SCORE_TAG]
        self.depression_profile[chat_id][DEPRESSION_CLASSIFICATION_TAG] = calculate_depression_class(depression_score)

    def send_statistics(self):
        logging.info('\n\nUsers Statistics:\n\n'
                     + '-> User Profiles:\n\n' + pprint.pformat(self.depression_profile) + '\n\n')

    def send_resources(self, chat_id):
        self.send_and_clear_custom_keyboard(chat_id, 'Aqui tienes algunos recursos que te podrian ser de utilidad')
        resources = self.resources_repository.provide()
        for resource in resources:
            if 'video' == resource['type']:
                params = dict(title=resource['title'], url=resource['url'])
                if 'description' in resource:
                    params['description'] = resource['description']
                    self.send(chat_id, COMPOUND_VIDEO_MESSAGE_TEMPLATE.safe_substitute(params))
                else:
                    self.send(chat_id, VIDEO_MESSAGE_TEMPLATE.safe_substitute(params))
