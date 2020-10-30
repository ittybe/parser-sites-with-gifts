# -*- coding: utf-8 -*-

# Done
from bs4 import BeautifulSoup as BS
import requests
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import config


class Oasiscatalog:
    def __init__(self):
        # not for category parsing
        # because tree with category names appears dynamically by clicking on element
        self.main_page = 'https://www.oasiscatalog.com/' 
        # create browser, in order to wait for loading page
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.browser = webdriver.Chrome(config.PATH_TO_CHROMEDRIVER,chrome_options=chrome_options)

    def get_loaded_page(self, url, by_what, name_of_by_what,delay = 3):
        self.browser.get(url)
        WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((by_what, name_of_by_what)))
        return self.browser.page_source      
    # done 
    def parser_category(self):
        cat_link = "https://www.oasiscatalog.com/categories/"

        # self.browser.get(cat_link)
        # self.browser.find_element(By.CLASS_NAME, "rubricator__desktop-toggler").click()

        r = requests.get(cat_link)
        html = BS(r.content, 'html.parser')
        categories = []

        for el in html.find_all(class_='subcats__link'):
            title = el.text.strip()
            href = el['href']

            subcat_link = "https://www.oasiscatalog.com"+ href
            self.browser.get(subcat_link)
            delay = 3
            WebDriverWait(self.browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'subcats__link')))
           
            sub_html = BS(self.browser.page_source, "html.parser")
            sub_els = sub_html.find_all(class_='subcats__link')

            subcategories = []
            for sub_el in sub_els:
                sub_title = sub_el.text.strip()
                sub_href = sub_el["href"]
                subcategories.append({'title': sub_title, 'href': sub_href })
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
                goods.append({'title': title.text.strip(),
                              'href': title['href'],
                              'vendor code': product_number})
            if not html.select('.pagination__item'):
                break
            check_page = html.select('.pagination__item')[-2].select('a')[0].text
            if str(i) == check_page:
                break
            else:
                i += 1
        return goods

    def parser_good(self, page):
        try:
            r = requests.get(page)
            html = BS(r.content, 'html.parser')
            main_good = self.pars_good_main(page)
            main_good['price'] = [main_good['price']]
            main_good['color'] = [main_good['color']]
            main_good['stocks'] = [main_good['stocks']]
            main_good['descript'] = [main_good['descript']]
            main_good['material'] = [main_good['material']]
            item_other_colors_box = html.select('.product-preview__colors-item')
            if item_other_colors_box:
                for item in item_other_colors_box[1:]:
                    other_colors = item.select('a')[0]
                    href_color = other_colors['href']
                    good_color = self.pars_good_main(self.main_page+href_color[1:])
                    main_good['price'].append(good_color['price'])
                    main_good['color'].append(good_color['color'])
                    main_good['stocks'].append(good_color['stocks'])
                    main_good['descript'].append(good_color['descript'])
                    main_good['material'].append(good_color['material'])
            return {'section': main_good['section'], 'name': main_good['name'], 'page': main_good['href'],
                    'marks': main_good['mark'], 'prices': main_good['price'], 'colors': main_good['color'],
                    'stock_availability': main_good['stocks'], 'descriptions': main_good['descript'],
                    'materials': main_good['material']}

        except Exception as ex:
            print("[EROR]*****************************************************")
            print(ex)
            print("[EROR]*****************************************************")

    # done
    def pars_good_main(self, page):
        html_tree = self.get_loaded_page(page, By.CLASS_NAME, "price")
        html = BS(html_tree , 'html.parser')
        name = html.select('.product-heading__title')[0].text.strip()
        # # with open("test.html", "w") as f:
        # #     f.write(str(html_tree))
        # print(name)
        price = float(html.select('.product-price2')[0].select('meta')[0]['content'])
        section = html.select('.breadcrumbs')[0].select('.breadcrumbs__item')[-2].select('span')[0].text
        marks = html.select('.product-heading__ribbon')
        if marks:
            marks = [marks[0].text.strip()]
        color = [el.select('.product-params__item-data')[0].text.strip()
                    for el in html.select('.product-params__item')
                    if el.select('.product-params__item-title')[0].text.strip() == 'Цвет товара']
        if color:
            color = color[0]
        href = page
        stock = html.select('.product-control__nav-tab-text2')
        if stock:
            stock = float(html.select('.product-control__nav-tab-text2')[0].text.strip().replace(' ', '').replace(u'\xa0', ''))
        elif html.select('.product-amount__item'):
            stock = sum([float(el.select('.product-amount__row-b')[0].select('span')[0].text.replace('шт.','').strip().replace(' ', '').replace(u'\xa0', ''))
                     for el in html.select('.product-amount__item')])
        material = [el.select('.product-params__item-data')[0].text.strip()
                    for el in html.select('.product-params__item')
                    if el.select('.product-params__item-title')[0].text.strip() == 'Материал товара']
        if material:
            material = material[0]
        descript = html.select('.product__description')
        if descript:
            descript = descript[0].text.strip()
        return {'name': name, 'price': price, 'section': section, 'mark': marks, 'color': color, 'href': href,
                'stocks': stock, 'material': material, 'descript': descript}


    # these async version of method for gui  
    async def parser_category_async(self):
        self.parser_category()

    async def parser_goods_async(self, href):
        self.parser_goods(href)

    async def parser_good_async(self, page):
        self.parser_good(page)
    
    async def pars_good_main_async(self, page):
        self.pars_good_main(page)