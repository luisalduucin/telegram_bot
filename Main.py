import sys
import time
import telepot
import os

token = os.getenv('TELEGRAM_ACCESS_TOKEN', '')
users = {}

def setOperationMode(operationMode, chat_id):
    if operationMode.startswith('/') and operationMode != '/change_mode':
        users[chat_id] = operationMode
        bot.sendMessage(chat_id, 'Modo de operacion ' + operationMode + ' activado')
    else:
        bot.sendMessage(chat_id, 'Selecciona un modo de operacion')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    mensaje = msg['text']
    if content_type == 'text':
        if chat_id not in users:
            setOperationMode(mensaje, chat_id)
        else:
            if msg['text'] == '/change_mode':
                users.pop(chat_id, None)
                setOperationMode(mensaje, chat_id)
            elif users[chat_id] == '/echo_mode':
                bot.sendMessage(chat_id, mensaje)
            elif users[chat_id] == '/debug_mode':
                print(content_type, chat_type, chat_id)
            elif users[chat_id] == '/witai_mode':
                bot.sendMessage(chat_id, 'En desarrollo')
            else:
                bot.sendMessage(chat_id, 'Ese modo de operacion no es valido')
    else:
        bot.sendMessage(chat_id, 'Ese modo tipo de mensaje no es valido')

if token == '':
	print('Set TELEGRAM_ACCESS_TOKEN env variable')
	exit()

bot = telepot.Bot(token)
bot.message_loop(handle)
print ('Listening ...')

while 1:
    time.sleep(10)
