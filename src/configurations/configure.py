import os
import logging
import configurations.environments as env
from dotenv import load_dotenv
from pathlib import Path
import telebot
import message_handlers.start_game_message_handler as start_game_message_handler
from telebot import TeleBot

import private.storage as storage

def add_env():
    '''
    Добавляет в приложении переменные окружения
    '''
    dotenv_path = Path.cwd() / '.env'
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    for env_name in env.items:
        if not os.getenv(env.items[env_name]):
            raise Exception(f'Environment variable {env_name} is not defined')
        env.items[env_name] = os.getenv(env.items[env_name])

def add_logging():
    '''
    Добавляет настройки логирования
    '''
    telebot.logger.setLevel(logging.INFO)


def add_telegram_bot():
    '''
    Добавляет телеграм-бота
    '''
    
    bot = telebot.TeleBot(env.items['telegram_bot_token'])
    add_message_handlers(bot)
    bot.skip_pending = True
    bot.polling()

def add_message_handlers(bot: TeleBot):
    """
    Добавляет обработчики входящих сообщений для телеграм бота
    """
    start_game_message_handler.init(bot)