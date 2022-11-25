from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import ContextTypes, ConversationHandler
import rsauce, time
from cr_config import restricted

CHOOSING_CATEGORY, CHOOSING_COIN, CHOOSING_SAUCE, CHOOSING_SOUP = range(4)
CHOOSING_HOT, CHOOSING_SALAD, CHOOSING_APPETIZER, CHOOSING_BAKERY = range(4, 8)
CHOOSING_DESSERT, COOKING = range(8, 10)

default_keyboard = [
    [InlineKeyboardButton("Случайные", callback_data="1"),
    InlineKeyboardButton("Соусы", callback_data="Соусы")],

    [InlineKeyboardButton("Бульоны и супы", callback_data="Бульоны и супы"),
    InlineKeyboardButton("Горячие блюда", callback_data="4")],

    [InlineKeyboardButton("Салаты", callback_data="5"),
    InlineKeyboardButton("Закуски", callback_data="6")],

    [InlineKeyboardButton("Выпечка", callback_data="7"),
    InlineKeyboardButton("Десерты", callback_data="8")]]
default_markup = InlineKeyboardMarkup(default_keyboard)

sauce_keyboard = [
    [InlineKeyboardButton("Домашний майонез", callback_data="Домашний майонез"),
    InlineKeyboardButton("Подлива", callback_data="2")],

    [InlineKeyboardButton("Салатная заправка", callback_data="3"),
    InlineKeyboardButton("Соус-дип", callback_data="4")],

    [InlineKeyboardButton("Сладкий соус", callback_data="5"),
    InlineKeyboardButton("Ягодный соус", callback_data="6")],

    [InlineKeyboardButton("Соус к мясу", callback_data="7"),
    InlineKeyboardButton("Соус к птице", callback_data="8")],

    [InlineKeyboardButton("Соус к рыбе", callback_data="9"),
    InlineKeyboardButton("Другие соусы", callback_data="10")],
    
    [InlineKeyboardButton("Главная", callback_data="Main")]]
sauce_markup = InlineKeyboardMarkup(sauce_keyboard)

def markups(subcategory) -> list:
    subcategory_keyboards = []
    for i in range(len(rsauce.subcategories[subcategory])):
        subcategory_keyboard = []
        for j in range(0,len(rsauce.subcategories[subcategory][i])):
            subcategory_keyboard.append([InlineKeyboardButton(rsauce.subcategories[subcategory][i][j],
                                                    callback_data=rsauce.subcategories[subcategory][i][j])])
        if i == 0:
            subcategory_keyboard.append([InlineKeyboardButton("Главная", callback_data="Main"),
                                                    InlineKeyboardButton("-->", callback_data="Next")])
        elif i == len(rsauce.subcategories[subcategory]) - 1:
            subcategory_keyboard.append([InlineKeyboardButton("<--", callback_data="Prev"),
                                                    InlineKeyboardButton("Главная", callback_data="Main")])
        else:
            subcategory_keyboard.append([InlineKeyboardButton("<--", callback_data="Prev"),
                                                    InlineKeyboardButton("Главная", callback_data="Main"),
                                                    InlineKeyboardButton("-->", callback_data="Next")])
        subcategory_keyboards.append(subcategory_keyboard)
    subcategory_markups = []
    for i in range(len(subcategory_keyboards)):
        subcategory_markups.append(InlineKeyboardMarkup(subcategory_keyboards[i]))
    return subcategory_markups

soup_keyboard = [
    [InlineKeyboardButton("Борщ", callback_data="1"),
    InlineKeyboardButton("Горячие супы", callback_data="2")],

    [InlineKeyboardButton("Бульоны", callback_data="3"),
    InlineKeyboardButton("Куриный бульон", callback_data="4")],

    [InlineKeyboardButton("Мясной бульон", callback_data="5"),
    InlineKeyboardButton("Овощной бульон", callback_data="6")],

    [InlineKeyboardButton("Рыбный бульон", callback_data="7"),
    InlineKeyboardButton("Молочный суп", callback_data="8")],

    [InlineKeyboardButton("Солянка", callback_data="9"),
    InlineKeyboardButton("Рыбный суп", callback_data="10")],
    
    [InlineKeyboardButton("Окрошка", callback_data="11"),
    InlineKeyboardButton("Рассольник", callback_data="12")],

    [InlineKeyboardButton("Суп-лапша", callback_data="13"),
    InlineKeyboardButton("Свекольник", callback_data="1")],

    [InlineKeyboardButton("Суп-пюре", callback_data="15"),
    InlineKeyboardButton("Другие супы", callback_data="16")],

    [InlineKeyboardButton("Главная", callback_data="Main")]]
soup_markup = InlineKeyboardMarkup(soup_keyboard)

def recipe_info(recipe: dict, step: int) -> list:
    image, title = recipe['image'], recipe['title']
    description, ingredients = recipe['description'], recipe['ingredients']
    steps = list()
    for s in range(step):
        steps.append(recipe[f'walkthrough{s+1}'])
    combined = [image, title, description, ingredients, steps]
    return combined

async def default(update, _):
    await update.message.reply_text("Выберите категорию:", reply_markup = default_markup)
    return CHOOSING_CATEGORY

async def choice(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()
    match variant:
        case "Соусы":
            await query.edit_message_text(text = f"Вы выбрали: {variant}.\nВыберите подкатегорию:",
                                    reply_markup = sauce_markup)
            return CHOOSING_SAUCE
        case "Бульоны и супы":
            await query.edit_message_text(text = f"Вы выбрали: {variant}.\nВыберите подкатегорию:",
                                    reply_markup = soup_markup)
            return CHOOSING_SOUP

cooking_markups = []

cooking_flag = ""
async def cooking(update, context):
    query = update.callback_query
    recipe = query.data
    await query.answer()
    # Здесь должна быть функция импорта рецепта с сайта с аргументом recipe_titles[variant].
    # Возвращает словарь с информацией о рецепте и количестве шагов приготовления.
    data = recipe_info(rsauce.julie, 5)
    global cooking_flag
    global active_sauce_page, active_subcategory, active_variant
    cooking_flag = recipe
    match cooking_flag:
        case "Main":
            if len(active_subcategory) > 0:
                if page_reset:
                    sauce_pages[active_variant] = 0
                else:
                    sauce_pages[active_variant] = active_sauce_page
                active_subcategory.clear()
                active_variant = ""
            await query.edit_message_text(text = "Выберите категорию:", reply_markup = default_markup)
            return CHOOSING_CATEGORY
        case "Prev":
            active_sauce_page -= 1
            mazik = f"Рецепты в данной категории:\nСтраница {active_sauce_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = mazik, reply_markup = active_subcategory[active_sauce_page])
            return COOKING
        case "Next":
            active_sauce_page += 1
            mazik = f"Рецепты в данной категории:\nСтраница {active_sauce_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = mazik, reply_markup = active_subcategory[active_sauce_page])
            return COOKING
        case "start":
            title = data[1]
            desc = data[2]
            message = title + "\n\nОписание:\n" + desc
            await context.bot.send_photo(chat_id = update.effective_chat.id,
                                            photo = data[0], caption = message)
            cooking_flag = "ingredient"
            return COOKING
        case "ingredient":
            ingredients = data[3].split("\n")
            message = "Ингредиенты:\n"
            for i in range(len(ingredients)):
                message += f"{i+1}. " + ingredients[i]
            context.bot.send_message(chat_id = update.effective_chat.id,
                                    text = message,
                                    )
    
async def coin() -> int:
    pass

page_reset = False

async def reset_page(update, _):
    global page_reset
    if page_reset is False:
        page_reset = True
        await update.message.reply_text("✅ Теперь страница подкатегории будет сбрасываться при возвращении в главное меню.")
    else:
        page_reset = False
        await update.message.reply_text("✅ Теперь страница подкатегории будет сохраняться при возвращении в главное меню.")

active_subcategory = list()
sauce_pages = {
    "Домашний майонез": 0, "Подлива": 0, "Салатная заправка": 0, "Соус-дип": 0, "Сладкий соус": 0,
    "Ягодный соус": 0, "Соус к мясу": 0, "Соус к птице": 0, "Соус к рыбе": 0, "Другие соусы": 0
}
active_sauce_page = 0
active_variant = ""
async def sauce(update, _) -> int:
    query = update.callback_query
    variant = query.data
    await query.answer()
    global active_sauce_page, active_subcategory, active_variant
    match variant:
        case "Main":
            if len(active_subcategory) > 0:
                if page_reset:
                    sauce_pages[active_variant] = 0
                else:
                    sauce_pages[active_variant] = active_sauce_page
                active_subcategory.clear()
                active_variant = ""
            await query.edit_message_text(text = "Выберите категорию:", reply_markup = default_markup)
            return CHOOSING_CATEGORY
        case "Домашний майонез":
            active_variant = variant
            active_subcategory = markups(variant)
            active_sauce_page = sauce_pages[variant]
            mazik = f"Рецепты в данной категории:\nСтраница {active_sauce_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = mazik, reply_markup = active_subcategory[active_sauce_page])
            return COOKING
        case "...": # Остальные подкатегории
            pass

async def soup(update, _) -> int:
    query = update.callback_query
    variant = query.data
    await query.answer()

    match variant:
        case "Main":
            await query.edit_message_text(text = "Выберите категорию:", reply_markup = default_markup)
            return CHOOSING_CATEGORY

async def hot() -> int:
    pass

async def salad() -> int:
    pass

async def appetizer() -> int:
    pass

async def bakery() -> int:
    pass

async def dessert() -> int:
    pass

@restricted
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<< ✅ Dialogue Terminated ✅ >>")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    time.sleep(1.5)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<< ✅ Allocated User Data Disintegrated ✅ >>")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    time.sleep(0.5)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="<< ⚠️ Execution Flag Set to False ⚠️ >>")
    return ConversationHandler.END
