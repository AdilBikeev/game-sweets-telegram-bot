import random
from telebot import TeleBot

import private.storage as storage

def init(bot: TeleBot):
    def process_digit_step(message):
        user_digit = message.text
        
        if not user_digit.isdigit():
                msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
                bot.register_next_step_handler(msg, process_digit_step)
                return

        attempt = storage.get(message.chat.id)["attempt"]
        random_digit = storage.get(message.chat.id)["random_digit"]

        if int(user_digit) == random_digit:
            bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
            storage.init(message.chat.id) ### Очищает значения из хранилище
            return
        elif attempt > 1:
            attempt-=1
            storage.set(message.chat.id, "attempt", attempt)
            bot.send_message(message.chat.id, f'Неверно, осталось попыток: {attempt}')
            bot.register_next_step_handler(message, process_digit_step)
        else:
            bot.send_message(message.chat.id, 'Вы проиграли!')
            storage.init(message.chat.id) ### Очищает значения из хранилище
            return

    @bot.message_handler(func=lambda message: message.text.lower() == "игра")
    def start_game(message):
        storage.init(message.chat.id) ### Инициализирую хранилище

        attempt = 5
        storage.set(message.chat.id, "attempt", attempt)

        bot.send_message(message.chat.id, f'Игра "угадай число"!\nКоличество попыток: {attempt}')

        random_digit=random.randint(1, 10)
        print(random_digit)

        storage.set(message.chat.id, "random_digit", random_digit)
        print(storage.get(message.chat.id))

        bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 10!')
        bot.send_message(message.chat.id, 'Введите число')
        bot.register_next_step_handler(message, process_digit_step)