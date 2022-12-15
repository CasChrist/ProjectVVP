#Содержит словари названий и адресов рецептов
from proreceip import keys
#Заполнение списка кнопок
buttons=[]
subcategory_content=[]
j=0
for i in range(len(keys)):
    subcategory_content.append(keys[i])
    if (i==18)or(i==27)or(i==35)or(i==37)or(i==54)or(i==75)or(i==85)or(i==108)or(i==141)or(i==155)or(i==158)or(i==162)or(i==164)or(i==171)or(i==181) :
        buttons.append(subcategory_content)
        j=j+1
        subcategory_content=[]
#Добавление названий категорий
buttons.insert(0, ["Случайный рецепт", "Бульоны и супы", "Горячие блюда", "Вторые блюда", "Салаты", "Консервы", "Закуски", "Соусы", "Выпечка", "Десерты", "Напитки", "Каши", "Украшения", "В пароварке", "Молочные продукты", "Маринад, панировка"])
