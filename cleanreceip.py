#Модуль предочистки словарей - удалить пустые и неправильно сверстанные рецепты
#Считать словари рецептов из файла receips.dat
import pickle
file=open("./Data/receips.dat", "rb")
loadsubcategories=pickle.load(file)
loadurlreceip=pickle.load(file)

#Очистка словарей - сократить до нужной длины, удалить ненужные
subcategories={}
urlreceip={}
delcat=[]
for key in loadsubcategories.keys():
    newkey=key
    newkey=newkey.replace("закусочные ", "")
    newkey=newkey.replace("Другие м", "М")
    #Удалить пустые, дублирующие и избыточные категории для упрощения пользовательского интерфейса
    #В т.ч. алкоголь, консервы, конину и аэрогриль
    if loadsubcategories[key][0][0]==str:
        delcat.append(newkey)
    else:   #Чтобы удаляемые ключи не дублировались
        if ("Горячие" in newkey)or("из" in newkey)or(" в " in newkey)or("Из " in newkey)or("лкогол" in newkey)or("онсерв" in newkey)or("онин" in newkey)or("грил" in newkey):
            delcat.append(newkey)
    subcategories[newkey]=loadsubcategories[key]
    urlreceip[newkey]=loadurlreceip[key]
#Обрезка лишних подкатегорий
for key in delcat:
    del subcategories[key]
    del urlreceip[key]

#Очистка рецептов, сверстанных через общие блоки, без шагов
from bs4 import BeautifulSoup
import requests
for key in subcategories.keys():
    n=3
    i=0
    while i<n:  #Перебор страниц ключа
        data=subcategories[key][i]
        m=5   #Перебор элементов страницы
        j=0
        while j<m:
            if data[j]==str:   #Удалить пустой элемент
                m=m-1   #Количество элементов на странице уменьшилось
                del subcategories[key][i][j]
                del urlreceip[key][i][j]
            else:   #Проверить верстку
                #Здесь считывание html-страницы
                page = requests.get(urlreceip[key][i][j])
                #проверка получения страницы, 200 = все хорошо, ij-номер рецепта
                print("Cat ", key, i+1, j+1, " connect: ", page.status_code)
                #Преобразую страницу в текст
                soup = BeautifulSoup(page.text, "html.parser")
                findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов
                if len(findsteps)==0:   #Удалить рецепт в случае верстки через общий блок
                    m=m-1   #Количество элементов на странице уменьшилось
                    del subcategories[key][i][j]
                    del urlreceip[key][i][j]
                else:
                    #Проверка верстки на корректное содержание текста
                    correct=0
                    for datastep in findsteps:
                        if datastep.find('p'):
                            correct=1
                    if correct==1:
                        #Перейти к следующему элементу
                        j=j+1
                    else:
                        m=m-1   #Количество элементов на странице уменьшилось
                        del subcategories[key][i][j]
                        del urlreceip[key][i][j]
        if len(data)==0:    #Если страница пуста, удалить ее
            n=n-1   #Количество страниц уменьшилось
            del subcategories[key][i]
            del urlreceip[key][i]
        else:   #Перейти к следующей странице
            i=i+1
#Удаление пустых ключей
empty_keys = []
for key in subcategories.keys():
    if len(subcategories[key])==0:
        empty_keys.append(key)
for key in empty_keys:
    del subcategories[key]
    del urlreceip[key]

#Запись очищенных словарей в файл
file=open("./Data/cleanreceips.dat", "wb")
pickle.dump(subcategories, file)
pickle.dump(urlreceip, file)
