from commands.help_command import help_command

# Словарь команд телеграм бота
commands = {
    # 'start': {  # command_name - название команды для телеграм бота
    #     'command_handler': start_command,  # обработчик команды
    #     'description': 'Отправляет приветственное сообщение'  # описание команды
    # },
    'help': {
        'command_handler': help_command,
        'description': 'Отображает список доступных команд'
    }
}
