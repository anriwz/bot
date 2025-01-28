import telebot 
from telebot import types

bot = telebot.Telebot('7529769115:AAGYwZ-EguZdAI7MwcWg3kjDWLOAEPTxO98')

@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    item1 = types.InlineKeyboardButton('Физика',callback_data = 'q1')
    item2 = types.InlineKeyboardButton('Математика',callback_data = 'q2')
    markup.add(item1,item2)

    bot.send_message(message.chat.id,'Привет! Я твой бот. Давай помогу решить задачу по:',reply_markup = markup)

bot.polling()

