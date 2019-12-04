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
            categories.append(title[0].text)


        return categories
