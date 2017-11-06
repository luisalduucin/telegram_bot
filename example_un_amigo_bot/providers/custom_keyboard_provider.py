import json
import os

from telepot.namedtuple import KeyboardButton


class CustomKeyboardProvider:
    def __init__(self):
        questions_file = open(os.path.dirname(__file__) + '/../data/questions.json', encoding='utf-8')
        questions = json.load(questions_file)
        questions_file.close()
        self.quick_responses_repository = {}
        for question_id, question_info in questions.items():
            quick_responses = {}
            for quick_response_id, quick_response_info in question_info['quick_responses'].items():
                quick_responses[quick_response_info['text']] = quick_response_info['value']
            self.quick_responses_repository[question_info['text']] = quick_responses

    def provide(self, question):
        keyboard = []
        for keyboard_button_text, keyboard_button_value in self.quick_responses_repository[question].items():
            keyboard.append(KeyboardButton(text=keyboard_button_text))
        return keyboard

    def get_button_value(self, question, response):
        return self.quick_responses_repository[question][response]
