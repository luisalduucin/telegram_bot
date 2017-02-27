import telepot
from pprint import pprint

bot = telepot.Bot('')
print(bot.getMe())

def handle(msg):
	pprint(msg)

bot.message_loop(handle)

