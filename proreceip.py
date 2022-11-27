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
        "step1":        'ExSt1NotFound'}
    #Где: картинка, название, описание, адрес рецепта на сайте, ингредиенты, шаги рецепта (дальше-больше)

    #Создаем url
    url=order
    if url==str:
        datarec["resource"]='UNKNOWN URL'
        return datarec

    #Здесь считывание html-страницы
    page = requests.get(url)
    #Проверка получения страницы, 200 = все хорошо
    print(page.status_code)
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

    #Возвращает в вызывающую функцию словарь рецепта
    return datarec

#Считать словари рецептов из файла receips.dat
import pickle
file=open("./Data/receips.dat", "rb")
subcategories=pickle.load(file)
urlreceip=pickle.load(file)