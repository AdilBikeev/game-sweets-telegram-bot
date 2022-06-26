from telegram import Update
from telegram.ext import ContextTypes

import private.menu as menu

async def help_command(update: Update, context: ContextTypes.context):
    """
    Обработчик команды /help
    """
    reply_text = menu.msg_all_commands()
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=reply_text)
