from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Токен бота (замените на ваш токен)
ТОКЕН = "ВАШ_ТОКЕН"

async def старт(update: Update, context: CallbackContext):
    """
    Обработка команды /start.
    """
    await update.message.reply_text("Привет! Я ваш телеграм-бот. Как я могу вам помочь?")

async def помощь(update: Update, context: CallbackContext):
    """
    Обработка команды /help.
    """
    текст_помощи = (
        "Доступные команды:\n"
        "/start - Начать диалог\n"
        "/help - Получить помощь\n"
        "/echo <текст> - Эхо-ответ"
    )
    await update.message.reply_text(текст_помощи)

async def эхо(update: Update, context: CallbackContext):
    """
    Обработка команды /echo.
    """
    текст = " ".join(context.args)  # Объединяем аргументы команды в строку
    if текст:
        await update.message.reply_text(f"Эхо: {текст}")
    else:
        await update.message.reply_text("Пожалуйста, укажите текст после команды /echo.")

async def обработать_сообщение(update: Update, context: CallbackContext):
    """
    Обработка текстовых сообщений.
    """
    текст = update.message.text
    await update.message.reply_text(f"Вы написали: {текст}")

def запустить_бота():
    """
    Запуск бота.
    """
    приложение = ApplicationBuilder().token(ТОКЕН).build()

    # Регистрация обработчиков команд
    приложение.add_handler(CommandHandler("start", старт))
    приложение.add_handler(CommandHandler("help", помощь))
    приложение.add_handler(CommandHandler("echo", эхо))
    приложение.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, обработать_сообщение))

    # Запуск бота
    print("Бот запущен...")
    приложение.run_polling()

if __name__ == "__main__":
    запустить_бота()
