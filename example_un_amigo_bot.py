import json
from example_un_amigo_bot.telegram_bot_impl import TelegramBotImpl

TELEGRAM_ENVIRONMENT_VAR = 'TELEGRAM_ACCESS_TOKEN'
WIT_AI_ENVIRONMENT_VAR = 'WIT_AI_ACCESS_TOKEN'
DEFAULT_VALUE = ''
BOT_NAME = 'Un amigo bot'

try:
    config_file = open('./config.local.json')
except OSError as err:
    print('\n\tError: execute `torus run node generateConfigs.js` to generate the config file\n')
    exit()
else:
    configs = json.load(config_file)

    telegram_access_token = configs[TELEGRAM_ENVIRONMENT_VAR]
    wit_access_token = configs[WIT_AI_ENVIRONMENT_VAR]

    bot = TelegramBotImpl(BOT_NAME, telegram_access_token, wit_access_token)
    bot.start()
