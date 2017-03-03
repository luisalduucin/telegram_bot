import os
from wit import Wit

access_token = os.getenv('WIT_AI_ACCESS_TOKEN', '')

if access_token == '':
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)

def send(request, response):
    print(response['text'])

def getPhrase(request, response):
        print(response)

actions = {
    'send': send,
    'getPhrase': getPhrase
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
