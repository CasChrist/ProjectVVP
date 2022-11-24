#библиотека python-telegram-bot 13.14
#конфигурация бота
from configtoken import mytoken #токен бота
from telegram.ext import Updater
TOKEN=mytoken
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
#конец конфигурации

#запуск выполнения бота
updater.start_polling()

#подключение обработчиков сообщений
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
#подключение инлайновых функций
from telegram import InlineQueryResultArticle, InputTextMessageContent

#определение команды старт
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I'm a bot, please talk to me!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
#определение команды, возвращающей файл с расписанием ФИТ-221
def shedule(update, context):
    document = 'https://kemsu.ru/upload/education/schedule/ic/och/IC_2c_fit-221,moa-221_4.pdf'
    context.bot.send_document(chat_id=update.effective_chat.id,
                             document=document)
shedule_handler = CommandHandler('shedule', shedule)
dispatcher.add_handler(shedule_handler)
#определение команды капс
def caps(update, context):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /caps argument')
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)
#определение ответа на любое текстовое сообщение
def echo(update, context):
    text = 'ECHO: ' + update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
#инлайновая команда капс
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Convert to UPPER TEXT',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)



#разработка функции вызова словаря рецепта
#подключение внешнего файла, содержащего массивы с именами рецептов и функцию поиска рецепта
import proreceip
#прототип вызывающей функции
def receip(update, context):
    #вызываем адрес рецепта по подкатегории и номеру
    #по дефолту (категория борщ, 3 строка, 4 столбец, "Жареный борщ")
    order = proreceip.urlreceip["Борщ"][2][3]
    #получаем словарь рецепта по адресу
    receipdata = proreceip.findreceip(order)
    #Здесь нужно преобразовать словарь рецепта в сообщение
    context.bot.send_photo(chat_id=update.effective_chat.id,
                             photo=receipdata['image'],
                             caption=receipdata['title'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=receipdata['description'])
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Источник рецепта:\n'+receipdata['resource'])                      
#срабатывает по команде /receip
receip_handler = CommandHandler('receip', receip)
dispatcher.add_handler(receip_handler)



#обработчик неизвестных команд, должен быть в конце!
# unknown must be in the end of program!
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)