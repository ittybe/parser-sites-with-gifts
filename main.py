# -*- coding: utf-8 -*-
# import main_window
import main_window_v2
from PyQt5 import QtWidgets
import sys
from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog
import xlwt

### Сделать так что бы виджеты были привязаны к combobox только один раз
class MainApp(QtWidgets.QMainWindow, main_window_v2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItem('https://happygifts.ru/')
        self.comboBox.addItem('https://gifts.ru/')
        self.comboBox.addItem('https://www.oasiscatalog.com/')
        self.happygifts = HappyGifts()
        self.gifts = Gifts()
        self.oasiscatalog = Oasiscatalog()
        self.pushButton.clicked.connect(self.update_categorie)
        self.listWidget.itemClicked.connect(self.remove_href)
        self.pushButton_5.clicked.connect(self.update_goods)
        self.pushButton_2.clicked.connect(self.add_in_outlist)
        self.pushButton_3.clicked.connect(self.parsing)
        self.categories = []
        self.goods = []

    def update_categorie(self):
        if self.comboBox.currentText() == 'https://happygifts.ru/':
            self.categories = self.happygifts.parser_category()
        elif self.comboBox.currentText() == 'https://gifts.ru/':
            self.categories = self.gifts.parser_category()
        elif self.comboBox.currentText() == 'https://www.oasiscatalog.com/':
            self.categories = self.oasiscatalog.parser_category()
        self.treeWidget.clear()
        self.listWidget_2.clear()
        for categorie in self.categories:
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            item.setText(0, categorie['title'])
            if categorie['subcategories']:
                for subcategorie in categorie['subcategories']:
                    sub_item = QtWidgets.QTreeWidgetItem(item)
                    sub_item.setText(0, subcategorie['title'])

    def update_goods(self):
        self.listWidget_2.clear()
        self.goods = []
        for item in self.treeWidget.selectedItems():
            for categorie in self.categories:
                if categorie['title'] == item.text(0):
                    goods = []
                    if self.comboBox.currentText() == 'https://happygifts.ru/':
                        goods = self.happygifts.parser_goods(categorie['href'])
                    elif self.comboBox.currentText() == 'https://gifts.ru/':
                        goods = self.gifts.parser_goods(categorie['href'])
                    elif self.comboBox.currentText() == 'https://www.oasiscatalog.com/':
                        goods = self.oasiscatalog.parser_goods(categorie['href'])
                    for good in goods:
                        self.goods.append(good)
                        self.listWidget_2.addItem(good['title'] + ' Артикул:' + good['vendor code'])
                else:
                    if categorie['subcategories']:
                        for subcategorie in categorie['subcategories']:
                            goods = []
                            if subcategorie['title'] == item.text(0):
                                if self.comboBox.currentText() == 'https://happygifts.ru/':
                                    goods = self.happygifts.parser_goods(subcategorie['href'])
                                elif self.comboBox.currentText() == 'https://gifts.ru/':
                                    goods = self.gifts.parser_goods(subcategorie['href'])
                                elif self.comboBox.currentText() == 'https://www.oasiscatalog.com/':
                                    goods = self.oasiscatalog.parser_goods(subcategorie['href'])
                                for good in goods:
                                    self.goods.append(good)
                                    self.listWidget_2.addItem(good['title'] + ' Артикул:' + good['vendor code'])

    def add_in_outlist(self):
        for select_item in self.listWidget_2.selectedItems():
            for good in self.goods:
                item = good['title'] + ' Артикул:' + good['vendor code']
                if item == select_item.text():
                    if self.comboBox.currentText() == 'https://happygifts.ru/':
                        self.listWidget.addItem('https://happygifts.ru/' + good['href'][1:])
                    elif self.comboBox.currentText() == 'https://gifts.ru/':
                        self.listWidget.addItem('https://gifts.ru/' + good['href'][1:])
                    elif self.comboBox.currentText() == 'https://www.oasiscatalog.com/':
                        self.listWidget.addItem('https://www.oasiscatalog.com/' + good['href'][1:])

    def parsing(self):
        goods = []
        for i in range(0, self.listWidget.count()):
            splited = self.listWidget.item(i).text().split('/')
            main_page = splited[0] + '//' + splited[2] + '/'
            if main_page == 'https://happygifts.ru/':
                good = self.happygifts.parser_good(self.listWidget.item(i).text())
                goods.append([main_page, good])
                print(good)
            elif main_page == 'https://gifts.ru/':
                good = self.gifts.parser_good(self.listWidget.item(i).text())
                goods.append([main_page, good])
                print(good)
            elif main_page == 'https://www.oasiscatalog.com/':
                good = self.oasiscatalog.parser_good(self.listWidget.item(i).text())
                goods.append([main_page, good])
                print(good)
        if goods:
            wb = xlwt.Workbook()
            sheets_pages = []
            sheets_object = []
            target_row = [1, 1, 1]
            try:
                for good in goods:
                    if good[0] not in sheets_pages:
                        sheets_pages.append(good[0])
                        sheets_object.append(wb.add_sheet(good[0].split('/')[-2]))
                    ws = sheets_object[sheets_pages.index(good[0])]
                    tr = target_row[sheets_pages.index(good[0])]
                    print(tr)
                    if tr == 1:
                        ws.write(tr, 0, 'Раздел')
                        ws.write(tr, 1, 'Наименование')
                        ws.write(tr, 2, 'Ссылка')
                        ws.write(tr, 3, 'Отметка')
                        ws.write(tr, 4, 'Цена')
                        ws.write(tr, 5, 'Цвет')
                        ws.write(tr, 6, 'Склад 1')
                        if good[0]=='https://happygifts.ru/':
                            ws.write(tr - 1, 6, '#Центральный')
                            ws.write(tr - 1, 7, '#Европа')
                            ws.write(tr - 1, 8, '#В пути')
                        ws.write(tr, 7, 'Склад 2')
                        ws.write(tr, 8, 'Склад 3')
                        ws.write(tr, 9, 'Описание')
                        ws.write(tr, 10, 'Материал')
                        target_row[sheets_pages.index(good[0])] += 1
                        tr += 1
                    for key, item in good[1].items():
                        if key == 'section':
                            ws.write(tr, 0, str(item))
                        elif key == 'name':
                            ws.write(tr, 1, str(item))
                        elif key == 'page':
                            ws.write(tr, 2, str(item))
                        elif key == 'marks':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 3, item[i])
                        elif key == 'prices':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 4, item[i])
                        elif key == 'colors':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 5, item[i])
                        # доработать(неправильно склады)
                        elif key == 'stock_availability':
                            if good[0]=='https://happygifts.ru/':
                                if item:
                                    for i in range(0, len(item)):
                                        for name, number in item[i].items():
                                            if name == 'Центральный':
                                                ws.write(tr + i, 6, number)
                                            elif name == 'В пути,':
                                                ws.write(tr + i, 8, number)
                                            elif name == 'Европа':
                                                ws.write(tr + i, 7, number)
                            if good[0] == 'https://gifts.ru/':
                                if item:
                                    for i in range(0, len(item)):
                                        ws.write(tr + i, 6, item[i])
                            if good[0] == 'https://www.oasiscatalog.com/':
                                if item:
                                    for i in range(0, len(item)):
                                        ws.write(tr + i, 6, item[i])
                        elif key == 'descriptions':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 9, str(item[i]))
                        elif key == 'materials':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 10, item[i])
                    target_row[sheets_pages.index(good[0])] += len(good[1]['colors'])
                wb.save('data.xls')
            except Exception as ex:
                print(ex)

    def remove_href(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
