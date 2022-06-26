import random
from tokenize import Number
from telebot import TeleBot

import private.storage as storage

def init(bot: TeleBot):
    MIN_SWEETS = 1
    MAX_SWEETS = 100

    def process_digit_step(message):
        user_digit = message.text
        count_sweets = storage.get(message.chat.id)["count_sweets"]

        if not user_digit.isdigit():
                msg = bot.reply_to(message, f'Ошибка ввода, пожалуйста введите число не более {count_sweets}')
                bot.register_next_step_handler(msg, process_digit_step)
                return
        
        if int(user_digit) == count_sweets: # Если пользователь забрал оставшиеся конфеты
            bot.send_message(message.chat.id, f'Ну все :( ты забрал оставшиеся конфеты. На столе ничего не осталось.')
            storage.init(message.chat.id) ### Очищает значения из хранилище
            return
        else: # Если конфеты ещё остались на столе
            offset = int(user_digit)
            count_sweets -= offset
            bot.send_message(message.chat.id, f'На столе осталось {count_sweets} конфет')

            offset = random.randint(MIN_SWEETS, count_sweets)
            count_sweets -= offset
            storage.set(message.chat.id, "count_sweets", count_sweets)
            bot.send_message(message.chat.id, f'"Компьютер с руками" забрал со стола {offset} конфет')
            
            if count_sweets != 0:
                bot.register_next_step_handler(message, process_digit_step)
                bot.send_message(message.chat.id, f'На столе ещё осталось {count_sweets} конфет, у тебя ещё есть все шансы выигарть!')
            else:
                bot.send_message(message.chat.id, f'Компьютер выиграл')
                storage.init(message.chat.id) ### Очищает значения из хранилище
                return

    @bot.message_handler(func=lambda message: message.text.lower() == "игра")
    def start_game(message):
        storage.init(message.chat.id) ### Инициализирую хранилище

        count_sweets = random.randint(MIN_SWEETS, MAX_SWEETS)
        storage.set(message.chat.id, "count_sweets", count_sweets)

        bot.send_message(message.chat.id, f"""
        Игра "Конфеты"!
        На столе лежит {count_sweets} конфет
        """)

        bot.send_message(message.chat.id, f"""
        Сколько конфет вы возьмете? (не более {count_sweets})
        """)

        bot.register_next_step_handler(message, process_digit_step)