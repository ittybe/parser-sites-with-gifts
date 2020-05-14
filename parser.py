import requests
from bs4 import BeautifulSoup
import re

def save_page(page: str, file_name: str):
    with open(file_name,'w', encoding='utf8') as html:
        html.write(page)


class Parser:
    def __init__(self):
        self.main_page = str()

    def __str__(self):
        return f'<parser {self.main_page}>'


class HappyGiftsParser(Parser):
    def __init__(self):
        super().__init__()
        self.main_page = 'https://happygifts.ru'

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

    def get_goods(self, categorie: dict):
        first_page = self.main_page + categorie['href']
        r = requests.get(first_page)
        soup = BeautifulSoup(r.content, 'html.parser')
        save_page(r.text, 'catalog.html')
        goods = []
        soup_section_id = soup.select_one('.catalog-sort-link.price.asc.active')['href']
        section_id = re.search(r'SECTION_ID=(\d+)&', soup_section_id).group(1)
        navigation = soup.select_one('.catalog-pagination')
        max_page = navigation.select('span')[-2].text
        if max_page == 'Вперед':
            max_page = 1
        else:
            max_page = int(max_page)
        print(f"{self.main_page} {categorie['title']}")
        for i in range(1, max_page + 1):
            page = f'{first_page}?PAGEN_1={i}&SECTION_ID={section_id}'
            print(page)
            r = requests.get(page)
            soup = BeautifulSoup(r.content, 'html.parser')
            for el in soup.select('li.catalog-item-container'):
                titles = el.select('.product-title')
                title = titles[0].text
                articules = el.select('.product-number')
                articule = articules[0]['title']
                if check_colors:
                    href = check_colors[0].select('.j_child')[0]['data-hash']
                else:
                    href = el.select('.catalog-grid-link')[0]['href']
                goods.append({'title': title, 'href': href, 'vendor code': product_number})
        return goods


if __name__ == '__main__':
    parser = HappyGiftsParser()
    print(parser)
    categories = parser.get_category()
    print(categories)
    for categorie in categories:
        print(parser.get_goods(categorie))