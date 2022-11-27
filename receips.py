#Массив рецептов на каждую подкатегорию
from bs4 import BeautifulSoup
import requests
#Функция формирует словари подкатегорий и адресов
def listreceip():
    url="https://www.povarenok.ru/recipes/cat/"
    list={}
    urls={}
    #Здесь считывание html-страницы
    page=requests.get(url)
    #проверка получения страницы, 200 = все хорошо
    print("Initiate list: ", page.status_code)
    #преобразую страницу в текст
    soup = BeautifulSoup(page.text, "html.parser")

    #Поиск имен рецептов
    finddiv=soup.findAll('div', class_='rubrics-bl')
    arrdiv=finddiv[0]
    for data in arrdiv:
        if data.find('span') is not None:
            spandel=arrdiv.select_one('span')
            if spandel is not None:
                spandel.decompose()
        if data.find('h2') is not None:
            htwodel=arrdiv.select_one('h2')
            if htwodel is not None:
                htwodel.decompose()
    arra=arrdiv.findAll('a')
    for data in arra:
        list[data.text]=[[str, str, str, str, str],
                         [str, str, str, str, str],
                         [str, str, str, str, str]]
        urls[data.text]=data.attrs['href']

    #Заполнение массивов для каждой страницы категории
    for caturl in urls:
        url=urls[caturl]
        urls[caturl]=[[str, str, str, str, str],
                      [str, str, str, str, str],
                      [str, str, str, str, str]]
        page=requests.get(url)
        #проверка получения страницы, 200 = все хорошо
        print("Cat connect: ", page.status_code)
        soup = BeautifulSoup(page.text, "html.parser")
        findartc=soup.findAll('article', class_='item-bl')
        i=0
        j=0
        for data in findartc:
            taga=data.find('h2').find('a')
            if j==5:
                j=0
                i=i+1
            list[caturl][i][j]=taga.text
            urls[caturl][i][j]=taga.attrs['href']
            j=j+1

    #Возвращает в вызывающую функцию словари имен, адресов
    return list, urls

subcategories, urlreceip = listreceip()
#Записать массивы в файл
import pickle
file=open("receips.dat", "wb")
pickle.dump(subcategories, file)
pickle.dump(urlreceip, file)