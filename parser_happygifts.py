from bs4 import BeautifulSoup as BS
import requests


class HappyGifts:
    def __init__(self):
        self.main_page = 'https://happygifts.ru/'

    def parser_category(self):
        r = requests.get(self.main_page)
        html = BS(r.content, 'html.parser')
        categories = []
        for el in html.select('.catalog-block'):
            title = el.select('.title')
            categories.append({'title': title[0].text, 'href': title[0]['href']})
        return categories

    def parser_goods(self, href):
        first_page = self.main_page + href[1:]
        r = requests.get(first_page)
        html = BS(r.content, 'html.parser')
        goods = []
        navigation = html.select('.catalog-pagination.modern-page-navigation')
        max_page = navigation[0].select('a')
        max_page = int(max_page[-2].text)
        for i in range(1, max_page+1):
            print('cтраница %i' %i)
            r = requests.get(first_page+'?PAGEN_1=' + str(i))
            html = BS(r.content, 'html.parser')
            for el in html.select('.catalog-item-container'):
                text_container = el.select('.text-container')
                if text_container:
                    title = text_container[0].select('.product-title')
                    goods.append({'title': title[0].text, 'href': title[0]['href']})
        print(goods)
        return goods