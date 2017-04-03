import os
from example_un_amigo_bot.telegram_bot_impl import TelegramBotImpl

TELEGRAM_ENVIRONMENT_VAR = 'TELEGRAM_ACCESS_TOKEN'
WIT_AI_ENVIRONMENT_VAR = 'WIT_AI_ACCESS_TOKEN'
DEFAULT_VALUE = ''
BOT_NAME = 'Un amigo bot'


def missing_env_var(env_var):
    print('Set ' + env_var + ' env variable')
    exit()


telegram_access_token = os.getenv(TELEGRAM_ENVIRONMENT_VAR, DEFAULT_VALUE)

if telegram_access_token == DEFAULT_VALUE:
    missing_env_var(TELEGRAM_ENVIRONMENT_VAR)

wit_access_token = os.getenv(WIT_AI_ENVIRONMENT_VAR, DEFAULT_VALUE)

if wit_access_token == DEFAULT_VALUE:
    missing_env_var(WIT_AI_ENVIRONMENT_VAR)

bot = TelegramBotImpl(BOT_NAME, telegram_access_token, wit_access_token)
bot.start()
