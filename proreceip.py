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
        "step1":        [[], '']}
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
    number=1    #Номер шага
    stepnumber='step1'  #Формовщик ключа
    stepimg=None   #Картинки шага
    findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов
    #Просмотр тегов шагов
    for data in findsteps:
        #Запись картинок
        if data.find('img'):
            stepimg=data.find('img').attrs['src']
            datarec[stepnumber][0].append(stepimg)
        else:
            stepimg=None
        #Запись текста
        steptext=data.find('p').text
        datarec[stepnumber][1]=steptext
        #Сохранение шагов, если есть текст
        if len(steptext)!=0:
            stepnumber=stepnumber.replace(str(number), str(number+1))
            #Создание экземпляра следующего шага
            datarec[stepnumber]=[[], '']
            number=number+1
            steptext=''
    #Удаление последнего прототипа шага (пустой)
    del datarec[stepnumber]

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
test=[]
delcat=[]
for key in loadsubcategories.keys():
    #Сократить названия ключей
    newkey=key
    newkey=newkey.replace("Фаршированная р", "Р")
    #Удалить рецепты c битыми картинками
    i=0
    for page in loadsubcategories[key]:
        j=0
        for elem in page:
            if ("ньок" in elem):
                loadsubcategories[key][i].pop(j)
            j+=1
            if len(loadsubcategories[key][i])==0:
                loadsubcategories[key].pop(i)
        i+=1
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
