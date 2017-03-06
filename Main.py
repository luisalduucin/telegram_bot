import sys
import time
import os

from telegram_api.TelegramBot import TelegramBot
from wit_ai_api.InteractiveWitClient import InteractiveWitClient

reload(sys)
sys.setdefaultencoding('utf8')

def setOperationMode(operationMode, chat_id):

    if operationMode.startswith('/') and operationMode != '/change_mode':
        
        activeUsers[chat_id] = {'operationMode' : operationMode}

        if operationMode == '/witai_mode':
                activeUsers[chat_id]['witClient'] = InteractiveWitClient(wit_access_token, actions)

        bot.send(chat_id, 'Modo de operacion ' + operationMode + ' activado')

    else:

        bot.send(chat_id, 'Selecciona un modo de operacion')

def botMsgHandler(msg):

    content_type, chat_type, chat_id = bot.glance(msg)
    mensaje = msg['text']
    user = activeUsers.get(chat_id, None)

    if content_type == 'text':

        if not user:
            setOperationMode(mensaje, chat_id)
        else:
            if msg['text'] == '/change_mode':

                activeUsers.pop(chat_id, None)
                setOperationMode(mensaje, chat_id)

            elif user['operationMode'] == '/echo_mode':

                bot.send(chat_id, mensaje)

            elif user['operationMode'] == '/debug_mode':

                print(content_type, chat_type, chat_id)

            elif user['operationMode'] == '/witai_mode':

                user['witClient'].talk(msg['text'])
                bot.send(chat_id, responseMsg[0])

            else:

                bot.send(chat_id, 'Ese modo de operacion no es valido')
    else:
        bot.send(chat_id, 'Ese tipo de mensaje no es valido')


telegram_access_token = os.getenv('TELEGRAM_ACCESS_TOKEN', '')

if telegram_access_token == '':
    print('Set TELEGRAM_ACCESS_TOKEN env variable')
    exit()

wit_access_token = os.getenv('WIT_AI_ACCESS_TOKEN', '')

if wit_access_token == '':
    print('Set WIT_AI_ACCESS_TOKEN env variable')
    exit()


''' TELEGRAM CLIENT INITIALIZATION '''

bot = TelegramBot(telegram_access_token, botMsgHandler)

''' WIT CLIENT CONFIGURATION '''

def send(request, response):
    responseMsg[0] = response.get('text', 'Error en el servicio de Wit.ai')

actions = { 'send': send }

activeUsers = {}
responseMsg = ['cadena']

while 1:
    time.sleep(10)
