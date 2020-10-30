from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog



gifts = Gifts()
print('[INFO] парсим категории gifts')
categories_g = gifts.parser_category()

goods_g = []

for good in goods_g:
    print('[INFO] парсим товар gifts ' + good['title'])
    good_out = gifts.parser_good('https://gifts.ru/' + good['href'][1:])
    goods_parsed.append(['https://gifts.ru/', good_out] )
    print('[INFO] товар плучен: ' + good['title'])
    if len(goods_parsed) == 80:
        break

exit()
happygifts = HappyGifts()
print('[INFO] парсим категории happygifts')
categories_h = happygifts.parser_category()
print('[INFO] категории:' + str(categories_h))
goods_h = []
for categorie in categories_h:
    print('[INFO] парсим каталог happygifts ' + categorie['title'])
    goods = happygifts.parser_goods(categorie['href'])
    for good in goods:
        goods_h.append(good)
goods_parsed = []
for good in goods_h:
    print('[INFO] парсим товар happygifts ' + good['title'])
    good_out = happygifts.parser_good('https://happygifts.ru/' + good['href'][1:])
    goods_parsed.append(['https://happygifts.ru/', good_out])
    print('[INFO] товар плучен: ' + good['title'])
    if len(goods_parsed) == 40:
        break
print(goods_parsed)

exit()

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