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

    #Поиск имен категорий рецептов
    finddiv=soup.findAll('div', class_='rubrics-bl')    #Найти контейнер со списком категорий
    arrdiv=finddiv[0]   #I don't know, but it is need
    for data in arrdiv:     #Просмотр каждого тега
        if data.find('span') is not None:   #Удаление имен глобальных разделов
            spandel=arrdiv.select_one('span')
            if spandel is not None:
                spandel.decompose()
        if data.find('h2') is not None:     #Удаление имен разделов
            htwodel=arrdiv.select_one('h2')
            if htwodel is not None:
                htwodel.decompose()
    arra=arrdiv.findAll('a')    #Поиск имен локальных подкатегорий
    for data in arra:   #Создание ключа с 15 рецептами
        list[data.text]=[[str, str, str, str, str],
                         [str, str, str, str, str],
                         [str, str, str, str, str]]
        urls[data.text]=data.attrs['href']  #Указание на адрес локальной подкатегории

    #Заполнение массивов имен и адресов для каждой страницы локальной подкатегории
    n=0
    for caturl in urls:
        url=urls[caturl]
        urls[caturl]=[[str, str, str, str, str],
                      [str, str, str, str, str],
                      [str, str, str, str, str]]
        page=requests.get(url)
        #проверка получения страницы, 200 = все хорошо
        print("Cat ", n, " connect: ", page.status_code)
        n=n+1   #Счетчик выполнения, т.к. оно идет ~5 минут
        soup = BeautifulSoup(page.text, "html.parser")
        findartc=soup.findAll('article', class_='item-bl')  #Поиск статей с рецептами
        i=0
        j=0
        for data in findartc:
            taga=data.find('h2').find('a')  #Поиск имени конкретного рецепта и его адреса
            if j==5:    #Запись в двумерный массив 3х5
                j=0
                i=i+1
            list[caturl][i][j]=taga.text
            urls[caturl][i][j]=taga.attrs['href']
            j=j+1

    #Возвращает в вызывающую функцию словари имен, адресов
    return list, urls

subcategories, urlreceip = listreceip()

#Записать массивы в файл receips.dat
import pickle
file=open("receips.dat", "wb")
pickle.dump(subcategories, file)
pickle.dump(urlreceip, file)