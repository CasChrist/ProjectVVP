#Содержит словари названий и адресов рецептов
from proreceip import keys
#Заполнение списка кнопок
buttons=[]
subcategory_content=[]
j=0
def save_category(subcategory_content, j):
    buttons.append(subcategory_content)
    j=j+1
    subcategory_content=[]
for i in range(len(keys)):
    subcategory_content.append(keys[i])
    if (i==18)or(i==50)or(i==75)or(i==92)or(i==114)or(i==145)or(i==155)or(i==180)or(i==215)or(i==224)or(i==229)or(i==244)or(i==247)or(i==257)or(i==276)or(i==283)or(i==305)or(i==316) :
        buttons.append(subcategory_content)
        j=j+1
        subcategory_content=[]
#Добавление названий категорий
buttons.insert(0, ["Случайный рецепт", "Бульоны и супы", "Горячие блюда", "Вторые блюда", "Салаты", "Консервы", "Закуски", "Соусы", "Выпечка", "Десерты", "В аэрогриле", "Алкоголь", "Напитки", "Каши", "Украшения", "В пароварке", "Молочные продукты", "В мультиварке", "Маринад, панировка"])
