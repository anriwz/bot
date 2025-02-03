from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters


# Определите функцию обработчика команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Определяем кнопки выбора предмета
    keyboard = [
        [InlineKeyboardButton("Математика", callback_data='math')],
        [InlineKeyboardButton("Физика", callback_data='physics')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Привет! Я твой бот. Какую задачу ты хочешь решить?', reply_markup=reply_markup)

# Функция для обработки нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем взаимодействие с кнопко

    # Проверяем, какую кнопку нажали
    if query.data == 'math':
        await query.edit_message_text(text="Вы выбрали Математику!")
        await show_additional_buttons(query)
    elif query.data == 'physics':
        await query.edit_message_text(text="Вы выбрали Физику!")
        await show_additional_buttons(query)

# Функция для показа дополнительных кнопок
async def show_additional_buttons(query) -> None:
    # Определяем дополнительные кнопки
    keyboard = [
        [InlineKeyboardButton("Фото", callback_data='photo')],
        [InlineKeyboardButton("Текст", callback_data='text')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text="Как вам будет удобнее отправить текст здачи:", reply_markup=reply_markup)

# Функция для обработки дополнительных кнопок
async def extra_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждаем взаимодействие с кнопкой
    # Сохраняем выбор пользователя
    context.user_data['user_choice'] = query.data

    if query.data == 'photo':
        await query.edit_message_text(text="Отправьте фото задачи:")
    elif query.data == 'text':
        await query.edit_message_text(text="Отправьте текст задачи:")

# Обработка текстового ввода
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_text("Хм... дай подумать")

#  Обработка отправки фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем файл фото
    photo_file = update.message.photo[-1].get_file() 
    # Сохранение фото
    file_path = f'photo_{update.message.chat.id}.jpg'
    await photo_file.download(file_path)  # Используем await
    await update.message.reply_text("Хм... дай подумать")

# Основная функция для запуска бота
def main() -> None:
    # Используйте ApplicationBuilder для создания приложения
    application = ApplicationBuilder().token("7529769115:AAGYwZ-EguZdAI7MwcWg3kjDWLOAEPTxO98").build()

    # Зарегистрируйте обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='math|physics'))  # Обработчик для выбора предметов
    application.add_handler(CallbackQueryHandler(extra_button_handler, pattern='photo|text'))  # Обработчик для дополнительных кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запустите бота
    application.run_polling()

if __name__ == '__main__':
    main()


