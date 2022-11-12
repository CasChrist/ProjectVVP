import telegram, telegram.ext

# Этапы/состояния разговора
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Age", "Favourite colour"],
    ["Number of siblings", "Something else..."],
    ["Done"]]

markup = telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)

def facts_to_str(user_data: dict[str, str]) -> str:
    # Вспомогательная функция для форматирования
    # собранной информации о пользователе
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def start(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> int:
    # Начало разговора, просьба ввести данные
    await update.message.reply_text(
        "Hi! My name is Doctor Kirigaya. Today is your first appointment. "
        "Please tell me something about yourself first.", reply_markup = markup)
    # Сообщаем 'ConversationHandler', что сейчас состояние 'CHOOSING'
    return CHOOSING

async def regular_choice(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> int:
    # Запрос информации о выбранном предопределённом выборе
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I'd love to hear about that!")
    return TYPING_REPLY

async def custom_choice(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> int:
    # Запрос описания пользовательской категории
    await update.message.reply_text("Alright, please send me the category first, for example \"Most impressive skill\"")
    return TYPING_CHOICE

async def received_information(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> int:
    # Сохранить информацию, предоставленную пользователем,
    # и запросить следующую категорию
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion on something.",
        reply_markup = markup)
    return CHOOSING

async  def done(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE) -> int:
    # Вывод собранной информации и завершение разговора
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I've learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup = telegram.ReplyKeyboardRemove())
    user_data.clear()
    # 'ConversationHandler.END' сообщает 'ConversationHandler' об окончании разговора
    return telegram.ext.ConversationHandler.END
