from bs4 import BeautifulSoup
import requests
#Функция возвращает словарь с рецептом
#Аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findreceip(order):
    #Словарь рецепта
    datarec={
        "image":        './Data/Image404.png',
        "title":        'ExTitNotFound',
        "description":  'ExDesNotFound',
        "resource":      order,
        "ingredients":  'ExIngNotFound', 
        "step1":        ['./Data/Image404.png', 'ExStsNotFound']}
    #Где: картинка, название, описание, адрес рецепта на сайте, ингредиенты, шаги рецепта (с картинкой)

    #Создаем url
    url=order
    #Если случайно запрошен пустой рецепт, то вернуть дефолтный словарь
    if url==str:
        datarec["resource"]='UNKNOWN URL'
        return datarec

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code, end = ': ')
    #Преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Картинка
    image = []
    findimgs=soup.findAll('img', itemprop='image')
    image=findimgs[0].attrs['src']
    datarec["image"]=image
    
    #Название
    title = []
        #На случай если нужно использовать другое поле
        #findtitle=soup.findAll('h1', itemprop='name')
        #for data in findtitle:
        #    title.append(data.text)
    title=findimgs[0].attrs['title']
    datarec["title"] = title
    
    #Описание
    description = []
    finddesc=soup.findAll('div', class_='article-text')
    for data in finddesc:
       if data.find('p') is not None:
           description.append(data.text)
    #Преобразовать описание в строку
    desctext=''
    for data in description:
        desctext=desctext+data
    datarec['description']=desctext
    
    #Ингредиенты
    datarec['ingredients']=''
    ingstags = []
    findings=soup.findAll('div', class_='ingredients-bl')
    arrdiv=findings[0]
    arrli=arrdiv.findAll('li')  #Поиск полей с текстом ингредиентов
    for data in arrli:
        ingstags.append(data.text)
    i=0
    for data in ingstags:   #Преобразование текстов в читаемый вид
        ingstags[i]=data.translate({ord('\n'):None})    #Убрать лишние переносы
        while "  " in ingstags[i]:      #Убрать лишние пробелы
            ingstags[i]=ingstags[i].replace("  ", " ")
        datarec['ingredients']=datarec['ingredients']+ingstags[i]+'\n'  #Записать ингредиенты построчно
        i=i+1
    datarec['ingredients']=datarec['ingredients'][:-1]

    #Шаги
    number=0    #Номер шага
    stepnumber='step0'  #Формовщик ключа
    stepimg='./Data/Image404.png'   #Картинка шага
    findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов
    if not findsteps:   #В случае верстки через общий блок (исключительный случай)
        finddiv=soup.findAll('div', itemtype="http://schema.org/Recipe")
        articlediv=finddiv[0]
        stepsdiv=articlediv.find('div', class_=None, id=None, itemprop=None)
        for data in stepsdiv:   #Перебор компонентов блока
            steptext=data.text
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера шага
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]
    else:   #Обычный случай пошаговой верстки
        for data in findsteps:
            if data.find('img').attrs['src']:   #Если найдена картинка
                stepimg=data.find('img').attrs['src']
            else:
                stepimg='./Data/Image404.png'
            steptext=data.find('p').text    #Запись текста
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]     #Сохранение списка картинка + текст шага

    #Возвращает в вызывающую функцию словарь рецепта
    return datarec



#####-#####

#Функция возвращает словарь с описанием рецепта
#Аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findrecdesc(order):
    #Словарь рецепта
    datarec={
        "image":        './Data/Image404.png',
        "title":        'ExTitNotFound',
        "description":  'ExDesNotFound',
        "resource":      order}
    #Где: картинка, название, описание, адрес рецепта на сайте

    #Создаем url
    url=order
    #Если случайно запрошен пустой рецепт, то вернуть дефолтный словарь
    if url==str:
        datarec["resource"]='UNKNOWN URL'
        return datarec

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code, end = ': ')
    #Преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Картинка
    image = []
    findimgs=soup.findAll('img', itemprop='image')
    image=findimgs[0].attrs['src']
    datarec["image"]=image
    
    #Название
    title = []
        #На случай если нужно использовать другое поле
        #findtitle=soup.findAll('h1', itemprop='name')
        #for data in findtitle:
        #    title.append(data.text)
    title=findimgs[0].attrs['title']
    datarec["title"] = title
    
    #Описание
    description = []
    finddesc=soup.findAll('div', class_='article-text')
    for data in finddesc:
       if data.find('p') is not None:
           description.append(data.text)
    #Преобразовать описание в строку
    desctext=''
    for data in description:
        desctext=desctext+data
    datarec['description']=desctext
    
    #Возвращает в вызывающую функцию словарь рецепта
    return datarec



#Функция возвращает словарь с ингредиентами
#Аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findrecings(order):
    #Словарь с ингредиентами
    datarec={
        "ingredients":  'ExIngNotFound'}

    #Создаем url
    url=order
    #Если случайно запрошен пустой рецепт, то вернуть дефолтный словарь
    if url==str:
        return datarec

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code, end = ': ')
    #Преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Ингредиенты
    datarec['ingredients']=''
    ingstags = []   #Список тегов, содержащих ингредиенты
    findings=soup.findAll('div', class_='ingredients-bl')
    arrdiv=findings[0]
    arrli=arrdiv.findAll('li')  #Поиск полей с текстом ингредиентов
    for data in arrli:
        ingstags.append(data.text)
    i=0
    for data in ingstags:   #Преобразование текстов в читаемый вид
        ingstags[i]=data.translate({ord('\n'):None})    #Убрать лишние переносы
        while "  " in ingstags[i]:      #Убрать лишние пробелы
            ingstags[i]=ingstags[i].replace("  ", " ")
        datarec['ingredients']=datarec['ingredients']+ingstags[i]+'\n'  #Записать ингредиенты построчно
        i=i+1
    datarec['ingredients']=datarec['ingredients'][:-1]

    #Возвращает в вызывающую функцию словарь с ингредиентами
    return datarec



#Функция возвращает словарь с шагами
#Аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findrecstps(order):
    #Словарь рецепта
    datarec={ 
        "step1":        ['./Data/Image404.png', 'ExStsNotFound']}
    #Где: шаги рецепта (с картинкой)

    #Создаем url
    url=order
    #Если случайно запрошен пустой рецепт, то вернуть дефолтный словарь
    if url==str:
        datarec["resource"]='UNKNOWN URL'
        return datarec

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code, end = ': ')
    #Преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Шаги
    number=0    #Номер шага
    stepnumber='step0'  #Формовщик ключа
    stepimg='./Data/Image404.png'   #Картинка шага
    findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов
    if not findsteps:   #В случае верстки через общий блок (исключительный случай)
        finddiv=soup.findAll('div', itemtype="http://schema.org/Recipe")
        articlediv=finddiv[0]
        stepsdiv=articlediv.find('div', class_=None, id=None, itemprop=None)
        for data in stepsdiv:   #Перебор компонентов блока
            steptext=data.text
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера шага
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]
    else:   #Обычный случай пошаговой верстки
        for data in findsteps:
            if data.find('img').attrs['src']:   #Если найдена картинка
                stepimg=data.find('img').attrs['src']
            else:
                stepimg='./Data/Image404.png'
            steptext=data.find('p').text    #Запись текста
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]     #Сохранение списка картинка + текст шага

    #Возвращает в вызывающую функцию словарь с шагами
    return datarec

#####-#####



#Считать словари рецептов из файла receips.dat
import pickle
file=open("./Data/receips.dat", "rb")
subcategories=pickle.load(file)
urlreceip=pickle.load(file)

'''
#Модуль очистки словарей - сократить до нужной длины, удалить пустые
for key in subcategories.keys():  #Перебор ключей
    if subcategories[key][0][0]==str:
        del subcategories[key]    #Удалить пустой ключ
        del urlreceip[key]
    else:
        i=0
        for data in subcategories[key]:     #Перебор элементов ключа
            j=0
            for elem in data:   #Удалить пустые
                if elem==str:
                    del subcategories[key][i][j]
                    del urlreceip[key][i][j]
                else:
                    j=j+1   #При удалении элемент стирается
            if len(data)!=0:
                i=i+1   #Если строка не пуста, перейти к следующему номеру
'''

#Словарь подкатегорий
keys={}
i=0
for key in subcategories.keys():
    keys[i]=key
    i=i+1
