from bs4 import BeautifulSoup as BS
import requests


class Gifts:
    def __init__(self):
        self.main_page = 'https://gifts.ru/'

    def parser_category(self):
        r = requests.get(self.main_page)
        html = BS(r.content, 'html.parser')
        categories = []
        for el in html.select('.catalog-section'):
            title = el.select('.catalog-section-name')[0].select('.catalog-section-link')[0].text
            href = el.select('.catalog-section-name')[0].select('a')[0]['href']
            list_item = el.select('.catalog-section-list')
            subcategories = []
            if list_item:
                for item in list_item:
                    subcategorie = item.select('a')
                    subcategories.append({'title': subcategorie[0].text, 'href': subcategorie[0]['href']})
            categories.append({'title': title, 'href': href, 'subcategories': subcategories})
        return categories

    def parser_goods(self, href):
        first_page = self.main_page + href[1:]
        r = requests.get(first_page)
        html = BS(r.content, 'html.parser')
        goods = []
        navigation = html.select('.paginator')
        if navigation:
            max_page = int(navigation[0].select('li')[-1].text)
        else:
            max_page = 1
        for i in range(1, max_page+1):
            print('cтраница %i' %i)
            r = requests.get(first_page+'/page' + str(i))
            html = BS(r.content, 'html.parser')
            for el in html.select('.j_parent'):
                title = el.select('.catalog-grid-name')[0].text
                product_number = el.select('.j_articlecode')[0].text.replace('Артикул: ', '')
                check_colors = el.select('.itm-clrs')
                if check_colors:
                    href = check_colors[0].select('.j_child')[0]['data-hash']
                else:
                    href = el.select('.catalog-grid-link')[0]['href']
                goods.append({'title': title, 'href': href, 'vendor code': product_number})
        return goods


    def parser_good(self,page):
        try:
            r = requests.get(page)
            html = BS(r.content, 'html.parser')
            main_good = self.pars_good_main(page)
            main_good['price'] = [main_good['price']]
            main_good['color'] = [main_good['color']]
            main_good['stocks'] = [main_good['stocks']]
            main_good['descript'] = [main_good['descript']]
            main_good['material'] = [main_good['material']]
            item_other_colors_box = html.select('.itm-clrs')
            if item_other_colors_box:
                other_colors = item_other_colors_box[0].select('a')
                for item in other_colors:
                    href_color = item['href']
                    good_color = self.pars_good_main(self.main_page+href_color[1:])
                    main_good['price'].append(good_color['price'])
                    main_good['color'].append(good_color['color'])
                    main_good['stocks'].append(good_color['stocks'])
                    main_good['descript'].append(good_color['descript'])
                    main_good['material'].append(good_color['material'])
            print(main_good)

            return {'section': main_good['section'], 'name': main_good['name'], 'page': main_good['href'],
                    'marks': main_good['mark'], 'prices': main_good['price'], 'colors': main_good['color'],
                    'stock_availability': main_good['stocks'], 'descriptions': main_good['descript'],
                    'materials': main_good['material']}

        except Exception as ex:
            print("[EROR]*****************************************************")
            print(ex)
            print("[EROR]*****************************************************")

    @staticmethod
    def pars_good_main(page):
        r = requests.get(page)
        html = BS(r.content, 'html.parser')
        name_block = html.select('.itm-hdr')[0].select('h1')[0].text
        if len(name_block.split(', ')) == 1:
            name = name_block.split(' ')[0]
        else:
            name = name_block.split(', ')[0]
        price = float(html.select('.j_price')[0].select('span')[0].text.replace(',', '.').replace(' ', ''))
        section = html.select('.itm-hdr')[0].select('li')[-3].select('span')[0].text
        mark = html.select('.btn.itm-lbl.color--danger')
        if mark:
            mark = [mark[0].text]
        if len(name_block.split(', ')) == 1:
            color = name_block.split(' ')[-1]
        else:
            color = name_block.split(', ')[-1]
        href = page
        stocks = sum([int(stock.select('.amount')[0].text)
                      for stock in html.select('.itm-ord-tbl')[0].select('.itm-ord-wh')])
        material = [opt.text.replace('Материал', '') for opt in html.select('.text_block')[0].select('li')
                    if opt.select('.itm-opts-label') if opt.select('.itm-opts-label')[0].text == 'Материал']
        if material:
            material = material[0]
        descript = html.select('#marketDescr')
        if descript:
            descript = descript[0].text
        else:
            descript = ''
        return {'name': name, 'price': price, 'section': section, 'mark': mark, 'color': color, 'href': href,
                'stocks': stocks, 'material': material, 'descript': descript}