import os
from example_echo_bot.telegram_bot_impl import TelegramBotImpl

TELEGRAM_ENVIRONMENT_VAR = 'TELEGRAM_ACCESS_TOKEN'
DEFAULT_VALUE = ''
BOT_NAME = 'Echo bot'


def missing_env_var(env_var):
    print('Set ' + env_var + ' env variable')
    exit()


telegram_access_token = os.getenv(TELEGRAM_ENVIRONMENT_VAR, DEFAULT_VALUE)

if telegram_access_token == DEFAULT_VALUE:
    missing_env_var(TELEGRAM_ENVIRONMENT_VAR)

bot = TelegramBotImpl(BOT_NAME, telegram_access_token)
bot.start()