from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog



oasiscatalog = Oasiscatalog()
good = oasiscatalog.pars_good_main("https://www.oasiscatalog.com/item/00000025135")
print(good)
exit()
print('[INFO] парсим категории oasiscatalog')


categories_o = oasiscatalog.parser_category()
print('[INFO] категории:' + str(categories_o))





goods_o = []
for categorie in categories_o:
    print('[INFO] парсим каталог oasiscatalog ' + categorie['title'])
    goods = oasiscatalog.parser_goods(categorie['href'])
    for good in goods:
        goods_o.append(good)
    print('[INFO] ' + categorie['title'] + ' товары получены')
    break
print(goods_o)