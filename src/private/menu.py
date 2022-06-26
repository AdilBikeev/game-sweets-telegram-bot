

def msg_all_commands():
    """
    Выводит все команды телеграм бота
    """

    from commands.entry import commands
    
    msg = ""
    command_names = commands.keys()
    for command_name in command_names:
        desc = commands[command_name]['description']
        msg += f"/{command_name} - {desc}\n"
    return msg