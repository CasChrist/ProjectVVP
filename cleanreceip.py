#Модуль предочистки словарей - удалить пустые и неправильно сверстанные рецепты
#Считать словари рецептов из файла receips.dat
import pickle
file=open("./Data/receips.dat", "rb")
loadsubcategories=pickle.load(file)
loadurlreceip=pickle.load(file)

from bs4 import BeautifulSoup
import requests

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
            else:   #Проверить верстку
                #Здесь считывание html-страницы
                page = requests.get(loadurlreceip[key][i][j])
                #проверка получения страницы, 200 = все хорошо, ij-номер рецепта
                print("Cat ", key, i+1, j+1, " connect: ", page.status_code)
                #Преобразую страницу в текст
                soup = BeautifulSoup(page.text, "html.parser")
                findsteps=soup.findAll('li', class_='cooking-bl')   #Поиск всех шагов
                if not findsteps:   #Удалить рецепт в случае верстки через общий блок
                    m=m-1   #Количество элементов на странице уменьшилось
                    del loadsubcategories[key][i][j]
                    del loadurlreceip[key][i][j]
                else:
                    correct=0
                    for datastep in findsteps:
                        if datastep.find('p'):
                            correct=1
                    if correct==1:
                        #Перейти к следующему элементу
                        j=j+1
                    else:
                        m=m-1   #Количество элементов на странице уменьшилось
                        del loadsubcategories[key][i][j]
                        del loadurlreceip[key][i][j]
        if len(data)==0:    #Если страница пуста, удалить ее
            n=n-1   #Количество страниц уменьшилось
            del loadsubcategories[key][i]
            del loadurlreceip[key][i]
        else:   #Перейти к следующей странице
            i=i+1
#Удаление пустых ключей
empty_keys = []
for key in loadsubcategories.keys():
    if len(loadsubcategories[key])==0:
        empty_keys.append(key)
for key in empty_keys:
    del loadsubcategories[key]
    del loadurlreceip[key]

#Запись очищенных словарей в файл
file=open("./Data/cleanreceips.dat", "wb")
pickle.dump(loadsubcategories, file)
pickle.dump(loadurlreceip, file)
