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
        max_page = navigation[0].select('li')
        if max_page:
            max_page = int(max_page[-1].text)
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

