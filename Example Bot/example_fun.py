#Библиотека python-telegram-bot 20.0a6
#Конфигурация бота
from secret_info import TOKEN #токен бота
from telegram.ext import ApplicationBuilder
application=ApplicationBuilder().token(TOKEN).build()
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
#Конец конфигурации

#Подключение обработчика сообщений-команд
from telegram.ext import CommandHandler

#Определение команды старт
async def start(update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="send command '/receip' to view receip")
start_handler=CommandHandler('start', start)
application.add_handler(start_handler)

#Шаблон вызова словаря рецепта
#Подключение внешнего файла, содержащего словари с рецептами и функцию поиска рецепта
import proreceip

#Подключение словарей рецептов и адресов
subcategories=proreceip.subcategories
urlrecip=proreceip.urlreceip

#Создание списка подкатегорий
listcat=[]
for key in subcategories.keys():
    listcat.append(key)

#Шаблон вызывающей функции
async def receip(update, context):
    #Вызываем адрес рецепта по подкатегории и номеру в массиве
    #По дефолту вызывает пустой рецепт
    order = proreceip.urlreceip[listcat[17]][0][1]
    
    #Получаем словарь рецепта по адресу
    receipdata = proreceip.findreceip(order)

    #Здесь нужно преобразовать словарь рецепта в сообщения
    #Описание словаря рецепта в файле rsauce
    
    await context.bot.send_photo(     #Картинка и название
        chat_id=update.effective_chat.id,
        photo=receipdata['image'],
        caption=receipdata['title'])
    
    await context.bot.send_message(   #Описание
        chat_id=update.effective_chat.id,
        text=receipdata['description'])
    
    await context.bot.send_message(   #Ингредиенты
        chat_id=update.effective_chat.id,
        text=receipdata['ingredients'])

    #Переслать все шаги
    number=1    
    stepnumber='step1'
    while stepnumber in receipdata:
        await context.bot.send_photo(     #Картинка и текст шага
            chat_id=update.effective_chat.id,
            photo=receipdata[stepnumber][0],
            caption=receipdata[stepnumber][1])
        stepnumber=stepnumber.replace(str(number), str(number+1))
        number=number+1
    
    await context.bot.send_message(   #Источник
        chat_id=update.effective_chat.id,
        text='Источник рецепта:\n'+receipdata['resource'])
               
#срабатывает по команде /receip
receip_handler=CommandHandler('receip', receip)
application.add_handler(receip_handler)

#запуск выполнения бота
application.run_polling()
