from bs4 import BeautifulSoup
import requests
#Функция возвращает словарь с рецептом
#аргумент - номер рецепта в массиве адресов urlnum
def findreceip(order):
    #Создаем url
    url="https://www.povarenok.ru/recipes/show/"+order
    #Здесь считывание html-страницы
    page = requests.get(url)
    #проверка получения страницы, 200 = все хорошо
    print(page.status_code)
    #преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")
    
    

    #словарь рецепта
    datarec = {"image": '', "title": '', "descriptiion": '', "resource": url}
    #где: картинка, название, описание, адрес рецепта на сайте

    

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



#Массивы для каждой категории записаны в отдельном файле
import receips
#Словарь с названиями всех категорий с именами рецептов
subcategories = {
    "Борщ": receips.soup_hot_borsh,
    "Щи": receips.soup_hot_shi,
    "Домашний майонез": receips.sauce_domashniy_maionez
    }
#Словарь адресов по категориям для вызова соответствующего рецепта (для функции)
urlreceip = {
    "Борщ": receips.urlnum_soup_hot_borsh,
    "Щи": receips.urlnum_soup_hot_shi,
    "Домашний майонез": receips.urlnum_sauce_domashniy_maionez
}