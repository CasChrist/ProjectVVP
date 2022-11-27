from bs4 import BeautifulSoup
import requests
#Функция возвращает словарь с рецептом
#аргумент - номер рецепта в массиве адресов urlnum (url адрес рецепта)
def findreceip(order):
    #Создаем url
    url=order
    #Здесь считывание html-страницы
    page = requests.get(url)
    #проверка получения страницы, 200 = все хорошо
    print(page.status_code)
    #преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #словарь рецепта
    datarec = {"image": '', "title": '', "descriptiion": '', "resource": url, "ingredients": 'example ingredients', 
               "step1": 'example step1'}
    #где: картинка, название, описание, адрес рецепта на сайте, ингредиенты, шаги рецепта (дальше-больше)

    #картинка
    image = []
    findimgs=soup.findAll('img', itemprop='image')
    image=findimgs[0].attrs['src']
    datarec["image"]=image
    
    #название
    title = []
        #на случай если нужно использовать другое поле
        #findtitle=soup.findAll('h1', itemprop='name')
        #for data in findtitle:
        #    title.append(data.text)
    title=findimgs[0].attrs['title']
    datarec["title"] = title
    
    #описание
    description = []
    finddesc=soup.findAll('div', class_='article-text')
    for data in finddesc:
       if data.find('p') is not None:
           description.append(data.text)
    #преобразовать описание в строку
    desctext=''
    for data in description:
        desctext=desctext+data
    datarec['description']=desctext
    
    #Возвращает в вызывающую функцию словарь рецепта
    return datarec

#Считать словари рецептов из файла receips.dat
import pickle
file=open("receips.dat", "rb")
subcategories=pickle.load(file)
urlreceip=pickle.load(file)