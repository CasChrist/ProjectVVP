#библиотека python-telegram-bot 13.14
#конфигурация бота
from secret_info import TOKEN #токен бота
from telegram.ext import Updater
TOKEN=TOKEN
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
#конец конфигурации

#запуск выполнения бота
updater.start_polling()

#подключение обработчика сообщений-команд
from telegram.ext import CommandHandler

#определение команды старт
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#разработка функции вызова словаря рецепта
#подключение внешнего файла, содержащего массивы с именами рецептов и функцию поиска рецепта
import rsauce, proreceip
#Подключение словарей рецептов и адресов
subcategories=rsauce.subcategories
urlrecip=rsauce.urlreceip
keys={} #Список подкатегорий
i=0
for key in subcategories.keys():
    keys[i]=key
    i=i+1

#прототип вызывающей функции
def receip(update, context):
    #вызываем адрес рецепта по подкатегории и номеру в массиве
    #по дефолту (категория борщ, 3 строка, 4 столбец, "Жареный борщ")
    order = rsauce.urlreceip[keys[0]][2][3]
    #получаем словарь рецепта по адресу
    receipdata = proreceip.findreceip(order)

    #Здесь нужно преобразовать словарь рецепта в сообщение
    context.bot.send_photo(chat_id=update.effective_chat.id,
                             photo=receipdata['image'],
                             caption=receipdata['title'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=receipdata['description'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=receipdata['ingredients']+'\n'+receipdata['step01'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Источник рецепта:\n'+receipdata['resource'])
               
#срабатывает по команде /receip
receip_handler = CommandHandler('receip', receip)
dispatcher.add_handler(receip_handler)