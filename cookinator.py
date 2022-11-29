import logging, cr_btn_menu
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler,
                          ConversationHandler, MessageHandler, filters)
from secret_info import TOKEN

logging.basicConfig(format = '%(asctime)s - [%(levelname)s] - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    message = "Бонжур! Я — Кукинатор. Моя задача — помочь вам приготовить кулинарный шедевр!\n\nВведите /begin чтобы открыть каталог рецептов."
    await context.bot.send_message(chat_id = update.effective_chat.id, text = message)

async def reject_begin(update, _):
    await update.message.reply_text("❌ Уже открыт один каталог. Зачем открывать второй точно такой же?")

async def reject_stop(update, _):
    await update.message.reply_text("❌ Нет-нет, этой командой меня не остановить. По крайней мере, не сейчас.")

async def unknown(update, _):
    await update.message.reply_text("Не знаю такой команды :(")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points = [CommandHandler("begin", cr_btn_menu.default)],
        states = {
            cr_btn_menu.CHOOSING_CATEGORY: [
                CallbackQueryHandler(cr_btn_menu.cooking, pattern = '^' + str(cr_btn_menu.buttons[0][0]) + '$'),
                CallbackQueryHandler(cr_btn_menu.choice)
            ],
            cr_btn_menu.COOKING: [
                CallbackQueryHandler(cr_btn_menu.cooking)
            ],
            cr_btn_menu.CATEGORY: [
                CallbackQueryHandler(cr_btn_menu.category)
            ],
                },
        fallbacks = [CommandHandler("stop", cr_btn_menu.done)])

    start_handler = CommandHandler("start", start)
    reject_begin_handler = CommandHandler("begin", reject_begin)
    reject_stop_handler = CommandHandler("stop", reject_stop)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    app.add_handler(start_handler)
    app.add_handler(conversation_handler)
    app.add_handler(reject_begin_handler)
    app.add_handler(reject_stop_handler)
    app.add_handler(unknown_handler)

    app.run_polling()