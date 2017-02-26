import telepot
from pprint import pprint

bot = telepot.Bot('330139199:AAHz0_U7_SShaJN4Sm1ZGOPUCZgSQ8J_RgA')
print(bot.getMe())

def handle(msg):
	pprint(msg)

bot.message_loop(handle)

