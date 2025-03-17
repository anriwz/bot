from openai import OpenAI
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from PIL import Image
import pytesseract

# Загрузка переменных окружения
load_dotenv()
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')  # Ваш API-ключ DeepSeek
bot_key = os.getenv('BOT_KEY')  # Токен Telegram-бота

# Инициализация клиента DeepSeek
client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

# Установите путь к Tesseract, если он не в PATH (для MacBook)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

# Функция для запроса к DeepSeek API
def ask_deepseek(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",  # Указанная в документации модель
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide detailed solutions to problems, ensuring that formulas and explanations are clear and easy to understand. Use plain text for formulas, avoiding complex Markdown or LaTeX. For example, write 'Q = m * c * (T2 - T1)' instead of 'Q = m \\cdot c \\cdot (T_2 - T_1)'."},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Математика", callback_data='math')],
        [InlineKeyboardButton("Физика", callback_data='physics')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Привет! Я твой бот. Какую задачу ты хочешь решить?', reply_markup=reply_markup)

# Функция для обработки нажатий кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'math':
        keyboard = [
            [InlineKeyboardButton("Текст", callback_data='math_text')],
            [InlineKeyboardButton("Фото", callback_data='math_photo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Вы выбрали Математику! Как вы хотите отправить задачу?", reply_markup=reply_markup)
    elif query.data == 'physics':
        keyboard = [
            [InlineKeyboardButton("Текст", callback_data='physics_text')],
            [InlineKeyboardButton("Фото", callback_data='physics_photo')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Вы выбрали Физику! Как вы хотите отправить задачу?", reply_markup=reply_markup)
    elif query.data in ['math_text', 'physics_text']:
        await query.edit_message_text(text="Отправьте текст задачи.")
    elif query.data in ['math_photo', 'physics_photo']:
        await query.edit_message_text(text="Отправьте фото задачи.")

# Обработка текстового ввода
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_text("Хм... дай подумать")

    try:
        # Используем DeepSeek API для решения задачи
        solution = ask_deepseek(f"Реши задачу: {user_text}. Предоставь подробное решение, объясни все шаги и формулы простым языком. Используй обычный текст для формул, например, 'Q = m * c * (T2 - T1)'.")

        # Отправляем решение
        await update.message.reply_text(solution)

    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при обработке задачи. Попробуйте еще раз.")

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Получаем фото
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive('user_photo.jpg')

    # Распознаем текст с фото
    text_from_photo = pytesseract.image_to_string(Image.open('user_photo.jpg'), lang='rus')

    if text_from_photo.strip() == "":
        await update.message.reply_text("Не удалось распознать текст на фото. Попробуйте еще раз.")
        return

    await update.message.reply_text("Текст распознан! Обрабатываю задачу...")

    try:
        # Используем DeepSeek API для решения задачи
        solution = ask_deepseek(f"Реши задачу: {text_from_photo}. Предоставь подробное решение, объясни все шаги и формулы простым языком. Используй обычный текст для формул, например, 'Q = m * c * (T2 - T1)'.")
        await update.message.reply_text(solution)
    except Exception as e:
        print(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при обработке задачи. Попробуйте еще раз.")

# Основная функция для запуска бота
def main() -> None:
    application = ApplicationBuilder().token(bot_key).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern='math|physics|math_text|math_photo|physics_text|physics_photo'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()