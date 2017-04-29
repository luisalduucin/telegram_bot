import json
import os


class QuestionsProvider:
    def __init__(self):
        questions_file = open(os.path.dirname(__file__) + '/../data/questions.json', encoding='utf-8')
        questions = json.load(questions_file)
        questions_file.close()
        self.questions_repository = []
        for question_id, question_info in questions.items():
            self.questions_repository.append(question_info['text'])

    def provide(self, index):
        return self.questions_repository[index]

    def are_remaining_questions(self, question_index):
        return question_index < len(self.questions_repository)
