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
        for data in stepsdiv:   #Перебор компонентов блока
            steptext=data.text
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера шага
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]
    else:   #Случай верстки через теги
        for data in findsteps:
            if data.find('img'):   #Если найдена картинка
                stepimg=data.find('img').attrs['src']
            else:
                stepimg=None
            steptext=data.find('p').text    #Запись текста
            stepnumber=stepnumber.replace(str(number), str(number+1))   #Переключение номера
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]     #Сохранение списка картинка + текст шага
    #Возвращает в вызывающую функцию словарь рецепта
    return datarec

#Считать словари рецептов из файла receips.dat
import pickle
file=open("./Data/receips.dat", "rb")
loadsubcategories=pickle.load(file)
loadurlreceip=pickle.load(file)

#Модуль очистки словарей - сократить до нужной длины, удалить пустые
#Удаление пустых ключей
empty_keys = []
for key in loadsubcategories.keys():
    if loadsubcategories[key][0][0]==str:
        empty_keys.append(key)
for key in empty_keys:
    del loadsubcategories[key]
    del loadurlreceip[key]
#Перебор ключей, удаление пустых значений
for key in loadsubcategories.keys():
    n=3
    i=0
    while i<n:  #Перебор страниц ключа
        data=loadsubcategories[key][i]
        m=5   #Перебор элементов страницы
        j=0
        while j<m:
            if data[j]==str:   #Удалить пустой элемент
                m=m-1   #Количество элементов на странице уменьшилось
                del loadsubcategories[key][i][j]
                del loadurlreceip[key][i][j]
            else:   #Перейти к следующему элементу
                j=j+1
        if len(data)==0:    #Если страница пуста, удалить ее
            n=n-1   #Количество страниц уменьшилось
            del loadsubcategories[key][i]
            del loadurlreceip[key][i]
        else:   #Перейти к следующей странице
            i=i+1
#Сокращение длины названий подкатегорий и запись в словари
subcategories={}
urlreceip={}
for key in loadsubcategories.keys():
    newkey=key
    newkey=newkey.replace("закусочные ", "")
    newkey=newkey.replace("Блюда из", "Из")
    newkey=newkey.replace("Горячие блюда", "Горячее")
    newkey=newkey.replace("Другие м", "М")
    newkey=newkey.replace(" в мультиварке", "")
    subcategories[newkey]=loadsubcategories[key]
    urlreceip[newkey]=loadurlreceip[key]

#Словарь подкатегорий по номерам
keys={}
i=0
for key in subcategories.keys():
    keys[i]=key
    i=i+1
