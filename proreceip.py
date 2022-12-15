from bs4 import BeautifulSoup
import requests
#Функция возвращает словарь с описанием рецепта
#Аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findreceip(order):
    #Словарь рецепта
    datarec={
        "current_step": 1,
        "image":        None,
        "title":        'ExTitNotFound',
        "description":  'ExDesNotFound',
        "resource":      order,
        "ingredients":  'ExIngNotFound', 
        "step1":        [None, 'ExStsNotFound']}
    #Где: картинка, название, описание, адрес рецепта на сайте, ингредиенты, шаги рецепта (с картинкой)

    #Создаем url
    url=order

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code, end = ': ')
    #Преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Картинка
    image = []
    findimgs=soup.findAll('img', itemprop='image')
    if findimgs:    #Если изображение есть, иначе без него
        image=findimgs[0].attrs['src']
        datarec["image"]=image
    
    #Название
    title = []
    title=findimgs[0].attrs['title']
    if title:
        datarec["title"] = title
    else:
        findtitle=soup.findAll('h1', itemprop='name')
        for data in findtitle:
            title.append(data.text)
    
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
    stepimg=None   #Картинка шага
    findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов

    if not findsteps:   #В случае верстки через общий блок
        finddiv=soup.findAll('div', itemtype="http://schema.org/Recipe")
        articlediv=finddiv[0]
        stepsdiv=articlediv.find('div', class_=None, id=None, itemprop=None)
        #Разделить блок на шаги по картинкам
        stepstext=stepsdiv.text.split("\r\n")
        #Удалить пустые сплиты
        k=0
        for data in stepstext:
            if data == '':
                stepstext.pop(k)
            k+=1
        #Компоновка рекламы
        k=0
        for data in stepstext:
            if data.find("Этот рецепт - участник акции") != -1:
                stepstext[k-1]+='\n'+stepstext.pop(k)
            k+=1
        #Запись картинок
        imgsstepsdiv=stepsdiv.findAll('div')
        stepsimgs=[]
        if imgsstepsdiv:
            for data in stepsdiv.findAll('div'):
                stepsimgs.append(data.find('img').attrs['src'])
        else:
            for data in stepsdiv.findAll('img'):
                stepsimgs.append(data.attrs['src'])
        #Сборка и сохранение шагов
        for data in stepstext:  
            steptext=data
            if number<len(stepsimgs):
                stepimg=stepsimgs[number]
            else:
                stepimg=None
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера шага
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]

    else:   #Случай верстки через теги
        #Просмотр тегов шагов
        for data in findsteps:
            #Запись картинки
            if data.find('img'):
                stepimg=data.find('img').attrs['src']
            else:
                stepimg=None
            #Запись текста
            steptext=data.find('p').text
            #Сохранение шагов
            stepnumber=stepnumber.replace(str(number), str(number+1))
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]
            
    #Возвращает в вызывающую функцию словарь рецепта
    return datarec

#Считать словари рецептов из файла ./Data/cleanreceips.dat
import pickle
file=open("./Data/cleanreceips.dat", "rb")
loadsubcategories=pickle.load(file)
loadurlreceip=pickle.load(file)

#Доочистка словарей - сократить до нужной длины, удалить ненужные
subcategories={}
urlreceip={}
delcat=[]
for key in loadsubcategories.keys():
    newkey=key
    newkey=newkey.replace("закусочные ", "")
    newkey=newkey.replace("Другие м", "М")
    #Удалить дублирующие и избыточные категории для упрощения пользовательского интерфейса
    #В т.ч. алкоголь, консервы, конину и аэрогриль
    if ("Горячие" in newkey)or("из" in newkey)or(" в " in newkey)or("Из " in newkey)or("лкогол" in newkey)or("онсерв" in newkey)or("онин" in newkey)or("грил" in newkey):
        delcat.append(newkey)
    else:   #Чтобы удаляемые ключи не дублировались
        if len(loadsubcategories[key])==0:
            delcat.append(newkey)
    subcategories[newkey]=loadsubcategories[key]
    urlreceip[newkey]=loadurlreceip[key]
#Обрезка лишних подкатегорий
for key in delcat:
    del subcategories[key]
    del urlreceip[key]

#Словарь подкатегорий по номерам
keys={}
i=0
for key in subcategories.keys():
    keys[i]=key
    i=i+1
