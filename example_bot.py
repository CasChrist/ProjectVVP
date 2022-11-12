"""
Асинхронный Telegram-бот на python-telegram-bot версии 20.х
"""

# импорт зависимых библиотек
import eb_config, logging, eb_btn_menu
from eb_btn_menu import facts_to_str, regular_choice, custom_choice, received_information, done, CHOOSING, TYPING_REPLY, TYPING_CHOICE, reply_keyboard, markup
from telegram import Update, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters

# подключаем журнал аудита (лог действий)
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    # ожидание отправки сообщения по сети - нужен оператор 'await'
    # 'bot.send_message' - это метод Telegram API
    # 'update.effective_chat.id' - определение 'id' чата, откуда поступил запрос
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "I'm a bot, please talk to me!")

# функция 'echo()' выводит пользователю его же сообщение от имени бота
async def echo(update, context):
    # 'update.message.text' - получить сообщение пользователя
    text = 'ECHO: ' + update.message.text
    await context.bot.send_message(chat_id = update.effective_chat.id, text = text)

# функция 'caps()' выводит пользователю его же сообщение в верхнем регистре
async def caps(update, context):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        await context.bot.send_message(chat_id = update.effective_chat_id, text = text_caps)
    else:
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "No command arguments detected.\nUsage: /caps (arguments)")

# функция 'unknown()' обрабатывает нераспознанные команды
async def unknown (update, context):
    await context.bot.send_message(chat_id = update.effective_chat.id, text = "Looks like you've entered a command I cannot recognize.")


# запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(eb_config.TOKEN).build()
    
    """ при получении запроса '/start' требуется вызвать функцию 'start()'
    start_handler = CommandHandler('start', start) """
    
    # при получении сообщения без '/' требуется вывести пользователю его же сообщение
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    # при получении запроса '/caps (arguments)' требуется вызвать функцию 'caps()'
    caps_handler = CommandHandler('caps', caps)

    # кнопочки
    conversation_handler = ConversationHandler(
        # точка входа в разговор
        entry_points = [CommandHandler("start", eb_btn_menu.start)],
        # словарь состояний разговора, возвращаемых callback функциями
        states = {
            # этап 'CHOOSING' - т.е. функция-обработчик какого-то сообщения явно
            # вернула константу 'CHOOSING' (return 'CHOOSING'), а так же послала/ответила
            # на сообщение. Ответ пользователя на это сообщение будет
            # обрабатываться хэндлерами, определёнными в этом списке
            CHOOSING: [
                    MessageHandler(filters.Regex("^(Age|Favourite colour|Number of siblings)$"), regular_choice),
                    MessageHandler(filters.Regex("^Something else...$"), custom_choice)],
            TYPING_CHOICE: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice)],
            TYPING_REPLY: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), received_information)]},
        # точка выхода из разговора
        fallbacks = [MessageHandler(filters.Regex("^Done$"), done)])

    # при получении неизвестного запроса требуется вызвать функцию 'unknown()'
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    # добавяем все хэндлеры в приложение
    #app.add_handler(start_handler)
    #app.add_handler(echo_handler)
    app.add_handler(caps_handler)
    app.add_handler(conversation_handler)
    
    # хэндлер неизвестных запросов добавлять в самом конце!
    app.add_handler(unknown_handler)
    
    app.run_polling()
