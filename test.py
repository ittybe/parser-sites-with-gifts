from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog
from main import MainApp
import xlwt

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
        goods_parsed.append(['https://happygifts.ru/', good_out])
        print('[INFO] товар плучен: ' + good['title'])
        if len(goods_parsed) == 40:
            break
    for good in goods_g:
        print('[INFO] парсим товар gifts ' + good['title'])
        good_out = gifts.parser_good('https://gifts.ru/' + good['href'][1:])
        goods_parsed.append(['https://gifts.ru/', good_out] )
        print('[INFO] товар плучен: ' + good['title'])
        if len(goods_parsed) == 80:
            break
    for good in goods_o:
        print('[INFO] парсим товар oasiscatalog ' + good['title'])
        good_out = oasiscatalog.parser_good('https://www.oasiscatalog.com/' + good['href'][1:])
        goods_parsed.append(['https://www.oasiscatalog.com/', good_out])
        print('[INFO] товар плучен: ' + good['title'])
        if len(goods_parsed) == 120:
            break
    print('[INFO] Запись в файл')
    parsing(goods_parsed)
    print('[INFO] Записано')


def parsing(goods):
    if goods:
        wb = xlwt.Workbook()
        sheets_pages = []
        sheets_object = []
        target_row = [1, 1, 1]
        try:
            for good in goods:
                print(good)
                if good[0] not in sheets_pages:
                    sheets_pages.append(good[0])
                    sheets_object.append(wb.add_sheet(good[0].split('/')[-2]))
                ws = sheets_object[sheets_pages.index(good[0])]
                tr = target_row[sheets_pages.index(good[0])]
                if tr == 1:
                    ws.write(tr, 0, 'Раздел')
                    ws.write(tr, 1, 'Наименование')
                    ws.write(tr, 2, 'Ссылка')
                    ws.write(tr, 3, 'Отметка')
                    ws.write(tr, 4, 'Цена')
                    ws.write(tr, 5, 'Цвет')
                    ws.write(tr, 6, 'Склад 1')
                    if good[0]=='https://happygifts.ru/':
                        ws.write(tr - 1, 6, '#Центральный')
                        ws.write(tr - 1, 7, '#Европа')
                        ws.write(tr - 1, 8, '#В пути')
                    ws.write(tr, 7, 'Склад 2')
                    ws.write(tr, 8, 'Склад 3')
                    ws.write(tr, 9, 'Описание')
                    ws.write(tr, 10, 'Материал')
                    target_row[sheets_pages.index(good[0])] += 1
                    tr += 1
                for key, item in good[1].items():
                    if key == 'section':
                        ws.write(tr, 0, str(item))
                    elif key == 'name':
                        ws.write(tr, 1, str(item))
                    elif key == 'page':
                        ws.write(tr, 2, str(item))
                    elif key == 'marks':
                        if item:
                            for i in range(0, len(item)):
                                ws.write(tr + i, 3, item[i])
                    elif key == 'prices':
                        if item:
                            for i in range(0, len(item)):
                                ws.write(tr + i, 4, item[i])
                    elif key == 'colors':
                        if item:
                            for i in range(0, len(item)):
                                ws.write(tr + i, 5, item[i])
                    # доработать(неправильно склады)
                    elif key == 'stock_availability':
                        if good[0]=='https://happygifts.ru/':
                            if item:
                                for i in range(0, len(item)):
                                    for name, number in item[i].items():
                                        if name == 'Центральный':
                                            ws.write(tr + i, 6, number)
                                        elif name == 'В пути,':
                                            ws.write(tr + i, 8, number)
                                        elif name == 'Европа':
                                            ws.write(tr + i, 7, number)
                        if good[0] == 'https://gifts.ru/':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 6, item[i])
                        if good[0] == 'https://www.oasiscatalog.com/':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 6, item[i])
                    elif key == 'descriptions':
                        if item:
                            for i in range(0, len(item)):
                                ws.write(tr + i, 9, str(item[i]))
                    elif key == 'materials':
                        if item:
                            for i in range(0, len(item)):
                                ws.write(tr + i, 10, item[i])
                print(good[0])
                if len(good[1]['colors'])>len(good[1]['marks']):
                    target_row[sheets_pages.index(good[0])] += len(good[1]['colors'])
                else:
                    target_row[sheets_pages.index(good[0])] += len(good[1]['marks'])
            wb.save('data.xls')
        except Exception as ex:
            print(ex)


test()