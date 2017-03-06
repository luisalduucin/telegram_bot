import telepot

class TelegramBot(object):

	def __init__(self, access_token, msgEventHandler):

		self.bot = telepot.Bot(access_token)
		self.bot.message_loop(msgEventHandler)
		print ('Bot listening ...')

	def glance(self, msg):

		return telepot.glance(msg)

	def send(self, chat_id, msg):

		self.bot.sendMessage(chat_id, msg)




