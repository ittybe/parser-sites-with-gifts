import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.main_page = str()

    def __str__(self):
        return f'<parser {self.main_page}>'


class HappyGiftsParser(Parser):
    def __init__(self):
        super().__init__()
        self.main_page = 'https://happygifts.ru/'

    def get_category(self):
        r = requests.get(self.main_page)
        html = BeautifulSoup(r.content, 'html.parser')
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


if __name__ == '__main__':
    parser = HappyGiftsParser()
    print(parser.get_category())