from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Определите функцию обработчика команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я твой бот.')

# Основная функция для запуска бота
def main() -> None:
    # Используйте ApplicationBuilder вместо Updater
    application = ApplicationBuilder().token("7529769115:AAGYwZ-EguZdAI7MwcWg3kjDWLOAEPTxO98").build()

    # Зарегистрируйте обработчик команды для команды /start
    application.add_handler(CommandHandler("start", start))

    # Запустите бота
    application.run_polling()

if __name__ == '__main__':
    main()


