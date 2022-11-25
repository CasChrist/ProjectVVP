from functools import wraps
from secret_info import LIST_OF_ADMINS, OWNER_ID
COMMANDS = {
    "user": ["help", "begin", "resetpage"],
    "admin": ["terminate", "toggleadmin"]
}

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

async def help(update, context):
    message = "Доступные команды:\n\n"
    for value in COMMANDS["user"]:
        message += f"/{value}\n"
    if update.effective_user.id in LIST_OF_ADMINS or update.effective_user.id == OWNER_ID:
        message += "\nAdministrative commands:\n\n"
        for value in COMMANDS["admin"]:
            message += f"/{value}\n"
    await context.bot.send_message(chat_id = update.effective_chat.id, text = message)

@restricted
async def toggle_admin(update, context):
    # print(LIST_OF_ADMINS)
    if context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            message = "❌ Failed to toggle admin rights for user: argument (user_id) must be an integer."
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