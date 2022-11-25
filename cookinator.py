import logging, cr_btn_menu
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler,
                          ConversationHandler, MessageHandler, filters)
from cr_config import restricted, help, toggle_admin
from secret_info import TOKEN

logging.basicConfig(format = '%(asctime)s - [%(levelname)s] - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

@restricted
async def reject_termination(update, context):
    await update.message.reply_text("❌ Access denied. The command can only be used when a 'telegram.ext.ConversationHandler' method is active.")

async def unknown(update, context):
    await update.message.reply_text("Не знаю такой команды :(")

buttons = [
    ["Случайные", "Соусы", "Бульоны и супы", "Горячие блюда",
    "Салаты", "Закуски", "Выпечка", "Десерты"],

    ["Домашний майонез", "Подлива", "Салатная заправка", "Соус-дип", "Сладкий соус",
    "Ягодный соус", "Соус к мясу", "Соус к птице", "Соус к рыбе", "Другие соусы"]
]

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points = [CommandHandler("begin", cr_btn_menu.default)],
        states = {
            cr_btn_menu.CHOOSING_CATEGORY: [
                # MessageHandler(filters.Regex("^Случайные$"), cr_btn_menu.coin),
                CallbackQueryHandler(cr_btn_menu.choice, pattern = '^' + str(buttons[0][1]) + '$'),
                CallbackQueryHandler(cr_btn_menu.choice, pattern = '^' + str(buttons[0][2]) + '$'),
                #MessageHandler(filters.Regex("^Горячие блюда$"), cr_btn_menu.hot),
                #MessageHandler(filters.Regex("^Салаты$"), cr_btn_menu.salad),
                #MessageHandler(filters.Regex("^Закуски$"), cr_btn_menu.appetizer),
                #MessageHandler(filters.Regex("^Выпечка$"), cr_btn_menu.bakery),
                #MessageHandler(filters.Regex("^Десерты$"), cr_btn_menu.dessert)
            ],
            cr_btn_menu.COOKING: [
                CallbackQueryHandler(cr_btn_menu.cooking),
            ],
            cr_btn_menu.CHOOSING_SAUCE: [
                CallbackQueryHandler(cr_btn_menu.sauce, pattern = "^Main$"),
                CallbackQueryHandler(cr_btn_menu.sauce, pattern = "^Prev$"),
                CallbackQueryHandler(cr_btn_menu.sauce, pattern = "^Next$"),
                CallbackQueryHandler(cr_btn_menu.sauce, pattern = "^Домашний майонез$"),
                # CallbackQueryHandler(cr_btn_menu.sauce),
            ],
            cr_btn_menu.CHOOSING_SOUP: [
                CallbackQueryHandler(cr_btn_menu.soup, pattern = "^Main$"),
            ],
                },
        fallbacks = [CommandHandler("terminate", cr_btn_menu.done)])

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    page_reset_handler = CommandHandler("resetpage", cr_btn_menu.reset_page)
    reject_termination_handler = CommandHandler("terminate", reject_termination)
    help_handler = CommandHandler("help", help)
    toggle_admin_handler = CommandHandler("toggleadmin", toggle_admin)
    app.add_handler(conversation_handler)
    app.add_handler(page_reset_handler)
    app.add_handler(reject_termination_handler)
    app.add_handler(help_handler)
    app.add_handler(toggle_admin_handler)
    app.add_handler(unknown_handler)

    app.run_polling()