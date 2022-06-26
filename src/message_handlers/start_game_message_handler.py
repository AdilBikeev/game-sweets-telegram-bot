import random
from tokenize import Number
from telebot import TeleBot

import private.storage as storage

def init(bot: TeleBot):
    # Значения для генерации изначального значения
    MIN_SWEETS = 1 # минимальное кол-во 🍬
    MAX_SWEETS = 100 # максимальное кол-во 🍬

    def process_digit_step(message):
        user_digit = message.text
        count_sweets = storage.get(message.chat.id)["count_sweets"]

        if (not user_digit.isdigit() or
            int(user_digit) < 1 or
            int(user_digit) > count_sweets):
                msg = bot.reply_to(message, f'Ошибка ввода, пожалуйста введите число не более {count_sweets}')
                bot.register_next_step_handler(msg, process_digit_step)
                return
        
        if int(user_digit) == count_sweets: # Если пользователь забрал оставшиеся 🍬ы
            bot.send_message(message.chat.id, f'Ты забрал оставшиеся 🍬ы и выиграл 🥳')
            storage.init(message.chat.id) ### Очищает значения из хранилище
            return
        else: # Если 🍬ы ещё остались на столе
            reply_text = []
            offset = int(user_digit)
            count_sweets -= offset
            reply_text.append(f'На столе осталось {count_sweets} 🍬')

            offset = random.randint(MIN_SWEETS, count_sweets)
            count_sweets -= offset
            storage.set(message.chat.id, "count_sweets", count_sweets)
            reply_text.append(f'"Компьютер с руками" забрал со стола {offset} 🍬')
            
            if count_sweets != 0: # Если 🍬ы ещё есть на столе
                bot.register_next_step_handler(message, process_digit_step)
                reply_text.append(f'На столе ещё осталось {count_sweets} 🍬, у тебя ещё есть все шансы выигарть!')
                reply_text.append(f'Сколько 🍬 вы возьмете? (не более {count_sweets})')
                bot.send_message(message.chat.id, '\n'.join(reply_text))
            else: # Если последние 🍬ы забрал компьютер
                reply_text.append(f'Компьютер выиграл 🥲')
                storage.init(message.chat.id) ### Очищает значения из хранилище
                bot.send_message(message.chat.id, '\n'.join(reply_text))
                return

    @bot.message_handler(func=lambda message: message.text.lower() == "start")
    def start_game(message):
        storage.init(message.chat.id) ### Инициализирую хранилище

        count_sweets = random.randint(MIN_SWEETS, MAX_SWEETS)
        storage.set(message.chat.id, "count_sweets", count_sweets)

        bot.send_message(message.chat.id, f"""
        Игра "Конфеты"!
        На столе лежит {count_sweets} 🍬
        """)

        bot.send_message(message.chat.id, f"""
        Сколько 🍬 вы возьмете? (не более {count_sweets})
        """)

        bot.register_next_step_handler(message, process_digit_step)