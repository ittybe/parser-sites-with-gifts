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


    def parser_good(self,page):
        try:
            r = requests.get(page)
            html = BS(r.content, 'html.parser')
            name_block = html.select('.itm-hdr')[0].select('h1')[0].text
            name = name_block.split(', ')[0]
            price = float(html.select('.j_price')[0].select('span')[0].text.replace(',', '.'))
            section = html.select('.itm-hdr')[0].select('li')[-3].select('span')[0].text
            mark = html.select('.btn.itm-lbl.color--danger')
            color = name_block.split(', ')[1]
            print(name)
            print(price)
            print(section)
            print(mark)
            print(color)
            stocks = html.select('.itm-ord-tbl')[0].select('')

            # prices = html.select('.product-settings-container')[0].select('.vu-price')
            # for price in prices:
            #     price_out = price.text
            #     price_out = price_out.replace('\n', '')
            #     price_out = price_out.strip()
            #     price_out = price_out.replace(' ', '')
            #     price_out = price_out.replace('Р', '')
            #     price_out = float(price_out)
            #     prices[prices.index(price)] = price_out
            # section = html.select('.breadcrumb-item.link-parent')[0].select('.breadcrumb-title')[0]['title']
            # marks = html.select('.icons-container')[0].select('span')
            # if marks:
            #     for mark in marks:
            #         if mark['class'][0] == "md_DownToZero":
            #             marks[marks.index(mark)] = mark['title']
            #         else:
            #             marks[marks.index(mark)] = mark.text
            # colors = html.select('.color-item')
            # for color in colors:
            #     colors[colors.index(color)] = color.select('div')[0]['data-title'].split(' (')[0]
            # # доработать(неправильно склады)
            # stock_availability = html.select('.avilability-numbers')
            # names_stock_availability = html.select('.avilability-tabs')
            # stock_out = []
            # for name_stock in names_stock_availability:
            #     names_tabs = name_stock.select('.avilability-tabs-item')
            #     for tab in names_tabs:
            #         names_tabs[names_tabs.index(tab)] = tab.select('span')[0].text
            #     names_stock_availability[names_stock_availability.index(name_stock)] = names_tabs
            # for stoks in stock_availability:
            #     stoks_ind = stoks.select('.number-all')
            #     for stock in stoks_ind:
            #         stoks_ind[stoks_ind.index(stock)] = int(stock.text)
            #     stock_availability[stock_availability.index(stoks)] = stoks_ind
            # for i in range(0, len(stock_availability)):
            #     dict_stock = {}
            #     for n in range(0, len(names_stock_availability[i])):
            #         if names_stock_availability[i][n] not in dict_stock:
            #             dict_stock[names_stock_availability[i][n]] = stock_availability[i][n]
            #         else:
            #             dict_stock[names_stock_availability[i][n]] += stock_availability[i][n]
            #     stock_out.append(dict_stock)
            # print(stock_out)
            # informations = html.select('.product-tab-blocks')
            # descriptions = []
            # materials = []
            # for information in informations:
            #     inf_select = information.select('h3')
            #     p_select = information.select('div')
            #     for inf in inf_select:
            #         if inf.text == 'Описание товара':
            #             output_text = ''
            #             for p in p_select[inf_select.index(inf)].select('p'):
            #                 output_text += p.text+' '
            #             descriptions.append(output_text)
            #         if inf.text == 'Характеристики':
            #             if len(p_select)==len(inf_select):
            #                 for p in p_select[inf_select.index(inf)].select('p'):
            #                     split_text = p.text.split(':', 1)
            #                     if split_text[0] == 'Материал':
            #                         materials.append(split_text[1])
            #             else:
            #                 for p in p_select[inf_select.index(inf)+1].select('p'):
            #                     split_text = p.text.split(':', 1)
            #                     if split_text[0] == 'Материал':
            #                         materials.append(split_text[1])
            #
            # return {'section': section, 'name': name, 'page': page, 'marks': marks,
            #         'prices': prices, 'colors': colors, 'stock_availability': stock_out,
            #         'descriptions': descriptions, 'materials': materials}

        except Exception as ex:
            print("[EROR]*****************************************************")
            print(ex)
            print("[EROR]*****************************************************")

