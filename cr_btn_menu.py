from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from proreceip import findreceip
from random import randint
from time import sleep
import proreceip

# Возвращаемые значения асинхронных функций, которые передаются в ConversationHandler.
CHOOSING_CATEGORY, CATEGORY, COOKING = range(0, 3)

# Названия категорий и подкатегорий.
buttons = [
    ["Случайный рецепт", "Соусы", "Бульоны и супы", "Горячие блюда",
    "Салаты", "Закуски", "Выпечка", "Десерты"],

    ["Домашний майонез", "Подлива", "Салатная заправка", "Соус-дип", "Сладкий соус",
    "Ягодный соус", "Соус к мясу", "Соус к птице", "Соус к рыбе", "Другие соусы"],

    ["Бульоны", "Куриный бульон", "Мясной бульон", "Овощной бульон", "Рыбный бульон",
    "Горячие супы", "Молочный суп", "Рыбный суп", "Борщ", "Окрошка", "Рассольник",
    "Свекольник", "Солянка", "Суп-лапша", "Суп-пюре", "Другие супы"],

    ["Блюда из мяса", "Блюда из птицы", "Горячие блюда из баранины", "Блюда из рыбы и морепродуктов", "Блюда из фарша", "Блюда из круп",
    "Блюда из овощей, грибов, бобовых", "Блюда из яиц", "Блюда на гриле", "Горячие блюда в горшочках", "Горячие блюда в казане",
    "Горячие блюда в микроволновке", "Горячие блюда из бобовых", "Вареники", "Гарнир", "Гарнир из круп"],

    ["Рыбные салаты", "Салаты из морепродуктов", "Салаты из баранины", "Салаты из ветчины", "Салаты из говядины",
    "Салаты из индейки", "Салаты из курицы", "Салаты из птицы", "Салаты из мяса", "Салаты из свинины", "Салаты из мясных субпродуктов",
    "Салаты из субпродуктов птицы", "Салаты из овощей, грибов, сыра", "Салаты из овощей",
    "Салаты из бобовых", "Салаты из рыбы и морепродуктов"],

    ["Бутерброды", "Горячие закуски", "Грибные закусочные торты", "Закуски из мяса", "Закрытый бутерброд",
    "Закуски из рыбы и морепродуктов", "Закуски из субпродуктов", "Закуски из овощей", "Закуски из сыра", "Закуски из яиц",
    "Закуски с грибами", "Закуски с колбасными изделиями", "Закуски с копченостями", "Закусочные кексы, маффины",
    "Закусочные рулеты", "Закусочные торты"],

    ["Бисквитное тесто", "Заварное тесто", "Дрожжевое тесто", "Блины", "Булочки",
    "Блины, оладьи, сырники", "Домашний хлеб", "Закуски из блинов", "Кексы", "Куличи",
    "Лаваш", "Лепешки", "Оладьи", "Начинка для блинов", "Изделия из теста", "Другие изделия"],

    ["Безе", "Желе", "Бисквитное печенье", "Бисквитный торт", "Вафли", "Гренки",
    "Десерты без выпечки", "Десертные крема", "Заварной торт", "Медовый торт",
    "Конфеты", "Мороженое", "Муссы", "Мюсли", "Другое", "Другие десерты"],
]

# Функция создаёт встроенную клавиатуру с категориями и подкатегориями.
def category_markups(category: str = "default") -> InlineKeyboardMarkup:
    # Сокращаем код. Подфункция создаёт массив с кнопками...
    def algorithm(index: int) -> list:
        category_keyboard = []
        # Если количество кнопок чётное:
        if len(buttons[index]) % 2 == 0:
                for i in range(0, len(buttons[index]), 2):
                    category_keyboard.append([InlineKeyboardButton(buttons[index][i], callback_data = buttons[index][i]),
                                InlineKeyboardButton(buttons[index][i+1], callback_data = buttons[index][i+1])])
                # Если НЕ главное меню (с категориями), добавить кнопку "Главная", т.е. возврат к списку категорий.
                if index != 0:
                    category_keyboard.append([InlineKeyboardButton("Главная", callback_data="Main")])
                return category_keyboard
        # Если количество кнопок нечётное:
        else:
            for i in range(0, len(buttons[index])-1, 2):
                category_keyboard.append([InlineKeyboardButton(buttons[index][i], callback_data = buttons[index][i]),
                            InlineKeyboardButton(buttons[index][i+1], callback_data = buttons[index][i+1])])
            category_keyboard.append([InlineKeyboardButton(buttons[index][len(buttons[index])-1], callback_data = buttons[index][len(buttons[index])-1])])
            if index != 0:
                category_keyboard.append([InlineKeyboardButton("Главная", callback_data="Main")])
            return category_keyboard
    keyboard = list()
    # ...в зависимости от переданного значения в основную функцию, вызывается соответствующая подфункция.
    match category:
        case "default":
            keyboard = algorithm(0)
        case "Соусы":
            keyboard = algorithm(1)
        case "Бульоны и супы":
            keyboard = algorithm(2)
        case "Горячие блюда":
            keyboard = algorithm(3)
        case "Салаты":
            keyboard = algorithm(4)
        case "Закуски":
            keyboard = algorithm(5)
        case "Выпечка":
            keyboard = algorithm(6)
        case "Десерты":
            keyboard = algorithm(7)
    # Возвращает объект 'InlineKeyboardMarkup', который является самой встроенной клавиатурой.
    category_markup = InlineKeyboardMarkup(keyboard)
    return category_markup

# Аналогично встроенные клавиатуры для страниц с рецептами в подкатегории.
def subcategory_markups(subcategory: str) -> list:
    subcategory_keyboards = []
    for i in range(len(proreceip.subcategories[subcategory])):
        subcategory_keyboard = []
        for j in range(0,len(proreceip.subcategories[subcategory][i])):
            subcategory_keyboard.append([InlineKeyboardButton(proreceip.subcategories[subcategory][i][j],
                                                    callback_data=f"start.{subcategory}.{i}.{j}")])
        if i == 0:
            subcategory_keyboard.append([InlineKeyboardButton("Главная", callback_data="Main"),
                                                    InlineKeyboardButton("-->", callback_data="Next")])
        elif i == len(proreceip.subcategories[subcategory]) - 1:
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

# Создаёт кнопки для самого рецепта. Без этой функции не получится посмотреть ингредиенты и шаги приготовления.
def recipe_markups(flag: str, step: int) -> list:
    keyboard = []
    match flag:
        case "start" | "start_random":
            keyboard.append([InlineKeyboardButton("Посмотреть ингредиенты", callback_data = "ingredient")])
            markup = InlineKeyboardMarkup(keyboard)
            return markup
        case "ingredient" | "step":
            keyboard.append([InlineKeyboardButton(f"Перейти к шагу {step}", callback_data = "step")])
            markup = InlineKeyboardMarkup(keyboard)
            return markup


# Функция входа в диалог. Выдаёт перечень категорий.
async def default(update, _):
    await update.message.reply_text("Выберите категорию:", reply_markup = category_markups())
    return CHOOSING_CATEGORY

# Информирует о выбранной категории и выдаёт клавиатуру с подкатегориями.
async def choice(update, _):
    query = update.callback_query
    variant = query.data
    await query.answer()
    await query.edit_message_text(text = f"Вы выбрали: {variant}.\nВыберите подкатегорию:",
                                    reply_markup = category_markups(variant))
    return CATEGORY

# Временные переменные для рецепта.
active_subcategory = list()
active_page = 0
active_variant = ""
cooking_flag = ""
current_step = 1
ingredient_triggered = False
data = dict()

# Подсказки для пользователя.
FINAL_MESSAGE = "\n\nНа этом всё... Приятного аппетита!"
HINT = "\n\n💡 Подсказка: Используйте /stop чтобы прекратить выполнение рецепта"
HINT_END = "💡 Подсказка: Используйте /begin для открытия каталога рецептов"

# Вызывается после выбора рецепта или по нажатии кнопки "Случайный рецепт" в списке категорий.
async def cooking(update, context):
    query = update.callback_query
    recipe = query.data.split('.')
    await query.answer()
    # "Импорт" временных переменных.
    global active_page, active_subcategory, active_variant
    global cooking_flag, current_step, ingredient_triggered, data
    # Ставим флаг в зависимости от того, выбран рецепт случайно или вручную.
    if recipe[0] == "Случайный рецепт":
        cooking_flag = "start_random"
    else:
        cooking_flag = recipe[0]
    match cooking_flag:
        # Если кнопкой вернулось это значение, сбросить временные переменные и вернуться к списку категорий.
        case "Main":
            active_subcategory.clear()
            active_variant = ""
            cooking_flag = ""
            current_step = 1
            active_page = 0
            ingredient_triggered = False
            data.clear()
            await query.edit_message_text(text = "Выберите категорию:", reply_markup = category_markups())
            return CHOOSING_CATEGORY
        # Открывает предыдущую страницу рецептов.
        case "Prev":
            active_page -= 1
            recipes = f"Рецепты в данной категории:\nСтраница {active_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = recipes, reply_markup = active_subcategory[active_page])
            return COOKING
        # Открывает следующую страницу рецептов.
        case "Next":
            active_page += 1
            recipes = f"Рецепты в данной категории:\nСтраница {active_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = recipes, reply_markup = active_subcategory[active_page])
            return COOKING
        # Срабатывает при выборе рецепта.
        case "start":
            # Импортирует URL рецепта из словаря 'urlreceip'. Аргументы: подкатегория, страница рецепта, номер рецепта на странице.
            receip = proreceip.urlreceip[recipe[1]][int(recipe[2])][int(recipe[3])]
            # Считывает всю информацию о рецепте в словарь.
            data = findreceip(receip)
            # Создаёт клавиатуру в зависимости от флага и номера шага.
            rm = recipe_markups(cooking_flag, current_step)
            title, description, source = data['title'].split(': '), data['description'], data['resource']
            # Вывод в консоль названия выбранных рецепта и подкатегории (для отладки).
            print(title[0] + ": " + title[1] + ". Подкатегория: " + recipe[1])
            message = title[1] + "\n\nОписание:\n" + description + "\n\nИсточник: " + source
            # Вывод пользователю картинки готового блюда, названия и краткого описания, а также ссылки на сайт.
            await context.bot.send_photo(chat_id = update.effective_chat.id,
                                            photo = data['image'], caption = message, reply_markup = rm)
            return COOKING
        # Срабатывает при нажатии "Случайный рецепт"
        case "start_random":
            # Аналогично 'start', только значения подбираются рандомно.
            subcat = proreceip.keys[randint(0, 331)]
            receip = proreceip.urlreceip[subcat][randint(0, 2)][randint(0, 4)]
            data = findreceip(receip)
            rm = recipe_markups(cooking_flag, current_step)
            title, description, source = data['title'].split(': '), data['description'], data['resource']
            print(title[0] + ": " + title[1] + ". Подкатегория: " + subcat)
            message = title[1] + "\n\nОписание:\n" + description + "\n\nИсточник: " + source
            await context.bot.send_photo(chat_id = update.effective_chat.id,
                                            photo = data['image'], caption = message, reply_markup = rm)
            return COOKING
        # Выводит пользователю список ингредиентов. Блокирует повторное нажатие кнопки "Посмотреть ингредиенты".
        case "ingredient":
            if ingredient_triggered is False:
                rm = recipe_markups(cooking_flag, current_step)
                ingredients = data['ingredients'].split("\n")
                message = "Ингредиенты:\n"
                for i in range(len(ingredients)):
                    message += f"{i+1}. " + ingredients[i] + "\n"
                message += HINT
                await context.bot.send_message(chat_id = update.effective_chat.id,
                                                text = message, reply_markup = rm)
                ingredient_triggered = True
                return COOKING
            return COOKING
        # Выводит пользователю шаги выполнения по одному.
        case "step":
            # Сброс переменных на последнем шаге и завершение диалога.
            if current_step == len(data) - 5:
                step_image = data[f"step{current_step}"][0]
                step_text = f"Шаг {current_step}\n" + data[f"step{current_step}"][1] + FINAL_MESSAGE
                await context.bot.send_photo(chat_id = update.effective_chat.id,
                                                photo = step_image, caption = step_text)
                sleep(0.5)
                await context.bot.send_message(chat_id = update.effective_chat.id,
                                                text = HINT_END)
                active_subcategory.clear()
                active_variant = ""
                cooking_flag = ""
                current_step = 1
                active_page = 0
                ingredient_triggered = False
                return ConversationHandler.END
            else:
                rm = recipe_markups(cooking_flag, current_step+1)
                step_image = data[f"step{current_step}"][0]
                step_text = f"Шаг {current_step}\n" + data[f"step{current_step}"][1]
                await context.bot.send_photo(chat_id = update.effective_chat.id,
                                                photo = step_image, caption = step_text, reply_markup = rm)
                current_step += 1
                return COOKING

# Выводит список подкатегорий. Игнорируется, если было выбрано "Случайный рецепт".
async def category(update, _) -> int:
    query = update.callback_query
    variant = query.data
    await query.answer()
    global active_page, active_subcategory, active_variant
    match variant:
        case "Main":
            await query.edit_message_text(text = "Выберите категорию:", reply_markup = category_markups())
            return CHOOSING_CATEGORY
        case _:
            active_variant = variant
            active_subcategory = subcategory_markups(variant)
            message = f"Рецепты в подкатегории {variant}:\nСтраница {active_page+1} из {len(active_subcategory)}"
            await query.edit_message_text(text = message, reply_markup = active_subcategory[active_page])
            return COOKING

# Принудительное завершение диалога и сброс временных переменных.
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global active_page, active_subcategory, active_variant
    global cooking_flag, current_step, ingredient_triggered
    active_subcategory.clear()
    active_variant = ""
    cooking_flag = ""
    current_step = 1
    active_page = 0
    ingredient_triggered = False
    data.clear()
    message = "✅ Выполнение рецепта прервано\n\n" + HINT_END
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ConversationHandler.END
