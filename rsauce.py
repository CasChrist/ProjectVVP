# Пример словаря для одного рецепта
julie = {
    'image' : 'https://www.povarenok.ru/data/cache/2012dec/17/25/51391_20516-710x550x.jpg',
    'title' : 'Соус а-ля майонез "Юлия" на молоке',
    'description' : 'Вот решила я как-то сделать майонез, просмотрела все рецепты и наткнулась в инете на такой необычный рецепт! Очень он меня заинтересовал тем, что в нем нет яйц и делается за несколько секунд!!!))) Ну думаю, сделаю, а то боялась делать обычный: там тонкой струйкой надо лить масло и взбивать несколько минут, да и яйца сырые смущают... а тут раз и за 5 секунд получается волшебство какое-то!!! Мне так понравилось!!! Вот решила и вам показать это чудо! И на вкус получается совсем не жирным, как может показаться на первый взгляд! Уверена на 100 %, что и у вас он получится без проблем - это так легко!!!)))',
    'resource' : 'https://www.povarenok.ru/recipes/show/34105/',
    'ingredients' : 'Молоко (у меня было 2,5% жирности, но жирность здесь не важна) — 150 мл\nМасло растительное (любое рафинированное) — 300 мл\nГорчица (готовая) — 2-3 ч. л.\nСок лимонный (можно заменить любым уксусом, например - яблочным или винным) — 1-2 ст. л.\nСоль (по вкусу) — 0,5 ч. л.',
    'step1' : 'Молоко комнатной температуры (это слова автора... но в комментариях девушки писали, что у них и с холодным получается), вылить в высокий стакан для блендера... А растительное масло можно брать любое! Первый раз я делала оливковое и подсолнечное в соотношении 1:1, а второй раз полностью из растительного - так мне понравилось больше! В общем с маслом можно экспериментировать - у всех ведь вкусы разные! ;-)',
    'step2' : 'Влить в стакан с молоком растительное масло...',
    'step3' : '... и взбить блендером (не миксером)...[color=g reen]буквально через 5-7 секунд вы увидите, как у вас получилась густая эмульсия!!![/color] Для меня это было чудо!!! :-) :-)',
    'step4' : 'Затем добавляем соль, лимонный сок и горчицу и снова взбиваем блендером 5 секунд! Всё!!! Выход пол литра)))',
    'step5' : '[color=blue]Попробуйте на вкус - может захочется добавить больше горчицы, соли, уксуса... или сахара по вкусу... В оригинальном рецепте вообще было 1 ч. л. соли, 3 ст. л. сока (или уксуса) и 1ст. л. горчицы, и когда я делала первый раз - майонез пересолился и перекислился! Второй раз я сделала всё по уму и результат мне очень понравился!!! ;-) И с лимонным соком мне больше понравилось, чем с уксусом! (первый раз я делала с яблочным уксусом)[/color] [color=green]В общем, дорогие мои, я вам даю супер идейку, а вы можете экспериментировать под свой вкус, добавляя разные специи, зелень и т. д. Девочки и мальчики удачи вам на кухне!!![/color] ;-) :-)',
}
# Где:
# image = ссылка на главную картинку
# title = название рецепта
# description = краткое описание (аннотация)
# resource = url рецепта
# ingredients = ингредиенты. Каждый ингредиент должен быть с новой строки!!!
# stepN = Ход приготовления, где N - от 1 до общего количества шагов.

#Считать словари рецептов из файла receips.dat
import pickle
file = open("receips.dat", "rb")
subcategories = pickle.load(file)
urlreceip = pickle.load(file)

keys = {} #Список подкатегорий
i = 0   #И их количество
for key in subcategories.keys():
    keys[i] = key
    i = i + 1
