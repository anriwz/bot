from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# Определите функцию обработчика команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Определяем кнопки
    keyboard = [
        [InlineKeyboardButton("Математика", callback_data='button1')],
        [InlineKeyboardButton("Физика", callback_data='button2')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Привет! Я твой бот. Какую задачу ты хочешь решить?', reply_markup=reply_markup)

# Функция для обработки нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем взаимодействие с кнопкой

    if query.data == 'button1':
        await query.edit_message_text(text="Вы нажали кнопку 1!")
    elif query.data == 'button2':
        await query.edit_message_text(text="Вы нажали кнопку 2!")

# Основная функция для запуска бота
def main() -> None:
    # Используйте ApplicationBuilder для создания приложения
    application = ApplicationBuilder().token("7529769115:AAGYwZ-EguZdAI7MwcWg3kjDWLOAEPTxO98").build()

    # Зарегистрируйте обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Запустите бота
    application.run_polling()

if __name__ == '__main__':
    main()



