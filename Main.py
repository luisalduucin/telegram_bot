import sys
import time
import telepot
import os

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

#TOKEN = sys.argv[1]  # get token from command-line
token = os.getenv('TELEGRAM_ACCESS_TOKEN', '')

if token == '':
	print('Set TELEGRAM_ACCESS_TOKEN env variable')
	exit()

bot = telepot.Bot(token)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
