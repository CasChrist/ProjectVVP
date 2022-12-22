import logging, cr_btn_menu
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler,
                          ConversationHandler, MessageHandler, filters)
from secret_info import TOKEN

# Лог действий (загрузка, ошибки и т.д.)
logging.basicConfig(format = '%(asctime)s - [%(levelname)s] - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# Файл, вызываемый по команде '/start'
async def start(update, context):
    message = "Бонжур! Я — Кукинатор. Моя задача — помочь вам приготовить кулинарный шедевр!\n\nВведите /begin чтобы открыть каталог рецептов."
    await context.bot.send_message(chat_id = update.effective_chat.id, text = message)

# Если уже запущен диалог, функция проинформирует об этом.
async def reject_begin(update, _):
    await update.message.reply_text("❌ Уже открыт один каталог.\nИспользуйте /stop чтобы прекратить выполнение рецепта")

# Если диалог не запущен, функция проинформирует об этом (загадочно).
async def reject_stop(update, _):
    await update.message.reply_text("❌ Нет-нет, этой командой меня не остановить. По крайней мере, не сейчас.\nВведите /begin чтобы открыть каталог рецептов.")

# Ответ на неизвестную команду с '/'
async def unknown(update, _):
    await update.message.reply_text("Не знаю такой команды :(\nВведите /begin чтобы открыть каталог рецептов.")

if __name__ == '__main__':
    # Создание бота через модуль telegram.ext. Токен берётся из файла secret_info.py
    app = ApplicationBuilder().token(TOKEN).build()

    # Сама начинка. Запускается командой '/begin', вызывает функцию 'default' из файла cr_btn_menu.py
    conversation_handler = ConversationHandler(
        entry_points = [CommandHandler("begin", cr_btn_menu.default)],
        states = {
            cr_btn_menu.CHOOSING_CATEGORY: [
                # Если выбрана кнопка "Случайный рецепт", сразу выдавать случайный рецепт, минуя стадию выбора подкатегории и рецепта.
                CallbackQueryHandler(cr_btn_menu.cooking, pattern = '^' + str(cr_btn_menu.buttons[0][0]) + '$'),
                # В противном случае вызываем список подкатегорий в выбранной категории.
                CallbackQueryHandler(cr_btn_menu.choice)
            ],
            cr_btn_menu.COOKING: [
                # Вызывает информацию о выбранном/случайном рецепте, ингредиентах и ходе приготовления.
                CallbackQueryHandler(cr_btn_menu.cooking)
            ],
            cr_btn_menu.CATEGORY: [
                # Открывает до 3 страниц с рецептами в данной подкатегории.
                CallbackQueryHandler(cr_btn_menu.category)
            ],
                },
        # Срабатывает при команде '/stop', принудительно завершает диалог.
        fallbacks = [CommandHandler("stop", cr_btn_menu.done)])

    # Обработчики на команды с '/'.
    start_handler = CommandHandler("start", start)
    reject_begin_handler = CommandHandler("begin", reject_begin)
    reject_stop_handler = CommandHandler("stop", reject_stop)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # Добавляем обработчики в программу бота.
    app.add_handler(start_handler)
    app.add_handler(conversation_handler)
    app.add_handler(reject_begin_handler)
    app.add_handler(reject_stop_handler)
    app.add_handler(unknown_handler)

    # Запускает бот и удерживает его в рабочем состоянии даже в случае вызова исключения.
    app.run_polling()