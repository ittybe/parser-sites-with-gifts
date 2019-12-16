from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog
from main import MainApp

def test():
    happygifts = HappyGifts()
    print('[INFO] парсим категории happygifts')
    categories_h = happygifts.parser_category()
    print('[INFO] категории:' + str(categories_h))
    gifts = Gifts()
    print('[INFO] парсим категории gifts')
    categories_g = gifts.parser_category()
    print('[INFO] категории:' + str(categories_g))
    oasiscatalog = Oasiscatalog()
    print('[INFO] парсим категории oasiscatalog')
    categories_o = oasiscatalog.parser_category()
    print('[INFO] категории:' + str(categories_o))
    goods_h = []
    for categorie in categories_h:
        print('[INFO] парсим каталог happygifts ' + categorie['title'])
        goods = happygifts.parser_goods(categorie['href'])
        for good in goods:
            goods_h.append(good)
        print('[INFO] ' + categorie['title'] + ' товары получены')
    goods_g = []
    for categorie in categories_g:
        print('[INFO] парсим каталог gifts ' + categorie['title'])
        goods = gifts.parser_goods(categorie['href'])
        for good in goods:
            goods_g.append(good)
        print('[INFO] ' + categorie['title'] + ' товары получены')
    goods_o = []
    for categorie in categories_o:
        print('[INFO] парсим каталог oasiscatalog ' + categorie['title'])
        goods = oasiscatalog.parser_goods(categorie['href'])
        for good in goods:
            goods_o.append(good)
        print('[INFO] ' + categorie['title'] + ' товары получены')
    goods_parsed = []
    for good in goods_h:
        print('[INFO] парсим товар happygifts ' + good['title'])
        good_out = happygifts.parser_good('https://happygifts.ru/' + good['href'][1:])
        goods_parsed.append([good_out, 'https://happygifts.ru/'])
        print('[INFO] товар плучен: ' + good['title'])
    for good in goods_g:
        print('[INFO] парсим товар gifts ' + good['title'])
        good_out = gifts.parser_good('https://gifts.ru/' + good['href'][1:])
        goods_parsed.append([good_out,'https://gifts.ru/'] )
        print('[INFO] товар плучен: ' + good['title'])
    for good in goods_o:
        print('[INFO] парсим товар oasiscatalog ' + good['title'])
        good_out = gifts.parser_good('https://www.oasiscatalog.com/' + good['href'][1:])
        goods_parsed.append([good_out, 'https://www.oasiscatalog.com/'])
        print('[INFO] товар плучен: ' + good['title'])
    print('[INFO] Запись в файл')
    MainApp().parsing(goods_parsed)
    print('[INFO] Записано')





test()