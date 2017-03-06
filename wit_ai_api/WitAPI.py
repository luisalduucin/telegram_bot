from wit import Wit

class WitAPI(object):

	def __init__(self, access_token, actions):

		self.access_token = access_token
		self.client = Wit(access_token = access_token, actions = actions)

	def analyze(self, msg):
		return self.client.message(msg)

	def getEntities(self, msg):
		return self.client.message(msg).get('entities', None)

	def talk(self, session_id, msg, context):
		response = self.client.run_actions(session_id, msg, context)
		print("Talk: " + str(response))
		return response

