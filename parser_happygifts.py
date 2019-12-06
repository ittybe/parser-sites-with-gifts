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
            list_item = el.select('.catalog-block-list-item')
            subcategories = []
            if list_item:
                for item in list_item:
                    subcategorie = item.select('a')
                    subcategories.append({'title': subcategorie[0].text, 'href': subcategorie[0]['href']})
            categories.append({'title': title[0].text, 'href': title[0]['href'], 'subcategories': subcategories})
        return categories

    def parser_goods(self, href):
        first_page = self.main_page + href[1:]
        r = requests.get(first_page)
        html = BS(r.content, 'html.parser')
        goods = []
        navigation = html.select('.catalog-pagination.modern-page-navigation')
        max_page = navigation[0].select('a')
        if max_page:
            max_page = int(max_page[-2].text)
        else:
            max_page = 1
        for i in range(1, max_page+1):
            print('cтраница %i' %i)
            r = requests.get(first_page+'?PAGEN_1=' + str(i))
            html = BS(r.content, 'html.parser')
            for el in html.select('.catalog-item-container'):
                text_container = el.select('.text-container')
                if text_container:
                    title = text_container[0].select('.product-title')
                    goods.append({'title': title[0].text, 'href': title[0]['href']})
        return goods

    def parser_good(self, href):
        page = self.main_page + href[1:]
        r = requests.get(page)
        html = BS(r.content, 'html.parser')
        name_block = html.select('#name_block_set0')
        name = name_block[0].select('h1')[0].text
        price = html.select('.vu-price')[0].text
        price = price.replace('\n', '')
        price = price.strip()
        price = price.replace(' ', '')
        price = float(price)
        try:
            settings = html.select('.product-tab-blocks')[0]
            headings = settings.select('h3')
            contents = settings.select('div')
            for content in contents:
                print(content['class'])

            print(len(contents))
            print(len(headings))
            for content in contents:
                print(content)
            # for head in headings:
            #     if head.text == 'Описание товара':
            #         description = contents[headings.index(head)]
            #         print(description)
        except Exception as ex:
            print('оШибка')
            print(ex)