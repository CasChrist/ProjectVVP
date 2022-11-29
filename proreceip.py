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
        "step1":        'ExStsNotFound'}
    #Где: картинка, название, описание, адрес рецепта на сайте, ингредиенты, шаги рецепта (дальше-больше)

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
    arrli=arrdiv.findAll('li')
    for data in arrli:
        ingstags.append(data.text)
    i=0
    for data in ingstags:
        ingstags[i]=data.translate({ord('\n'):None})
        while "  " in ingstags[i]:
            ingstags[i]=ingstags[i].replace("  ", " ")
        datarec['ingredients']=datarec['ingredients']+ingstags[i]+'\n'
        i=i+1

    #Шаги
    number=0
    stepnumber='step0'
    stepimg='./Data/Image404.png'
    findsteps=soup.findAll('li', class_='cooking-bl')
    if not findsteps:
        finddiv=soup.findAll('div', itemtype="http://schema.org/Recipe")
        articlediv=finddiv[0]
        stepsdiv=articlediv.find('div', class_=None, id=None, itemprop=None)
        for data in stepsdiv:
            steptext=data.text
            stepnumber=stepnumber.replace(str(number), str(number+1))
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]
    else:
        for data in findsteps:
            if data.find('img').attrs['src']:
                stepimg=data.find('img').attrs['src']
            steptext=data.find('p').text
            stepnumber=stepnumber.replace(str(number), str(number+1))
            number=number+1
            datarec[stepnumber]=[stepimg, steptext]

    #Возвращает в вызывающую функцию словарь рецепта
    return datarec