page_reset = False
# Функция переключает режим сохранения последней открытой страницы каталога
async def reset_page(update, _):
    global page_reset
    if page_reset is False:
        page_reset = True
        await update.message.reply_text("✅ Теперь страница подкатегории будет сбрасываться при возвращении в главное меню.")
    else:
        page_reset = False
        await update.message.reply_text("✅ Теперь страница подкатегории будет сохраняться при возвращении в главное меню.")

sauce_pages = {
    "Домашний майонез": 0, "Подлива": 0, "Салатная заправка": 0, "Соус-дип": 0, "Сладкий соус": 0,
    "Ягодный соус": 0, "Соус к мясу": 0, "Соус к птице": 0, "Соус к рыбе": 0, "Другие соусы": 0
}

from functools import wraps
def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_name = update.effective_user.name
        user_id = update.effective_user.id
        if user_id == OWNER_ID:
            return await func(update, context, *args, **kwargs)
        elif user_id not in LIST_OF_ADMINS:
            print(f"Access denied for {user_name}. Administrator rights required. User id:", user_id)
            await update.message.reply_markdown_v2(text = f"❌ *Access denied for {user_name}\. Administrator rights required\.*")
            return
        else:
            return await func(update, context, *args, **kwargs)
    return wrapped

from secret_info import LIST_OF_ADMINS, OWNER_ID
# Функция выдаёт/забирает несистемные права администратора бота
@restricted
async def toggle_admin(update, context):
    # print(LIST_OF_ADMINS)
    if context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            message = "❌ Failed to toggle admin rights for user: argument 'user_id' must be an integer."
            await context.bot.send_message(chat_id = update.effective_chat.id, text = message)
            return
        except:
            message = f" Failed to toggle admin rights for user due to an unknown error."
            await context.bot.send_message(chat_id = update.effective_chat.id, text = message)
            return
        if user_id == OWNER_ID:
            message = f"❌ This user is my owner. I can't do that."
            await context.bot.send_message(chat_id = update.effective_chat.id, text = message)
        elif user_id not in LIST_OF_ADMINS:
            LIST_OF_ADMINS.append(user_id)
            message = f"✅ User #{user_id} has been appointed as an administrator."
            await context.bot.send_message(chat_id = update.effective_chat.id, text = message)
        else:
            LIST_OF_ADMINS.remove(user_id)
            message = f"✅ User #{user_id} is no longer an administrator."
            await context.bot.send_message(chat_id = update.effective_chat.id, text = message)
    else:
        message = f"Usage: /toggleadmin (user_id)"
        await context.bot.send_message(chat_id = update.effective_chat.id, text = message)

COMMANDS = {
    "user": ["help", "begin", "stop"],
    "admin": ["terminate"]
}

async def help(update, context):
    message = "Доступные команды:\n\n"
    for value in COMMANDS["user"]:
        message += f"/{value}\n"
    if update.effective_user.id in LIST_OF_ADMINS or update.effective_user.id == OWNER_ID:
        message += "\nAdministrative commands:\n\n"
        for value in COMMANDS["admin"]:
            message += f"/{value}\n"
    await context.bot.send_message(chat_id = update.effective_chat.id, text = message)

# Пускай будет, может ещё пригодится
def recipe_info(recipe: dict, step: int) -> list:
    image, title = recipe['image'], recipe['title']
    description, ingredients = recipe['description'], recipe['ingredients']
    steps = list()
    for s in range(step):
        steps.append(recipe[f'walkthrough{s+1}'])
    combined = [image, title, description, ingredients, steps]
    return combined