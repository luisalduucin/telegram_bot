from wit import Wit


class WitAi(object):

    __ENTITIES_TAG = 'entities'
    __DEFAULT = None

    def __init__(self, access_token, actions):
        self.__wit_client = Wit(access_token, actions)

    def analyze(self, msg):
        return self.__wit_client.message(msg)

    def get_entities(self, msg):
        return self.__wit_client.message(msg).get(self.__ENTITIES_TAG, self.__DEFAULT)

    def talk(self, session_id, msg, context):
        return self.__wit_client.run_actions(session_id, msg, context)
