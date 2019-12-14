from bs4 import BeautifulSoup as BS
import requests


class Oasiscatalog:
    def __init__(self):
        self.main_page = 'https://www.oasiscatalog.com/'

    def parser_category(self):
        r = requests.get(self.main_page)
        html = BS(r.content, 'html.parser')
        categories = []
        for el in html.select('.rubricator__l1-item'):
            title = el.select('.rubricator__l1-link')[0].select('.rubricator__l1-item-text')[0].text
            href = el.select('.rubricator__l1-link')[0]['href']
            list_item = el.select('.rubricator__l2-link')
            subcategories = []
            if list_item:
                for item in list_item:
                    subcategorie = item
                    subcategories.append({'title': subcategorie.text.lstrip().rstrip(), 'href': subcategorie['href']})
            categories.append({'title': title, 'href': href, 'subcategories': subcategories})
        return categories

    def parser_goods(self, href):
        first_page = self.main_page + href[1:]
        goods = []
        i = 1
        while True:
            print('cтраница %i' % i)
            r = requests.get(first_page + '?page=' + str(i))
            html = BS(r.content, 'html.parser')
            for el in html.select('.catalog__product'):
                title = el.select('.catalog-product__title')[0]
                product_number = el.select('.catalog-product__article')[0].text
                goods.append({'title': title.text.lstrip().rstrip(),
                              'href': title['href'],
                              'vendor code': product_number})
            check_page = html.select('.pagination__item')[-2].select('a')[0].text
            if str(i) == check_page:
                break
            else:
                i += 1
        return goods