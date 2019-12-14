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