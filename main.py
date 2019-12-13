# -*- coding: utf-8 -*-
# import main_window
import main_window_v2
from PyQt5 import QtWidgets
import sys
from parser_happygifts import HappyGifts
import xlwt


class MainApp(QtWidgets.QMainWindow, main_window_v2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItem('https://happygifts.ru/')
        self.pushButton.clicked.connect(self.update_categorie)
        # self.treeWidget.itemClicked.connect(self.update_goods)
        self.listWidget.itemClicked.connect(self.remove_href)
        self.pushButton_5.clicked.connect(self.update_goods)
        self.pushButton_2.clicked.connect(self.add_in_outlist)
        self.pushButton_3.clicked.connect(self.parsing)
        self.categories = []
        self.goods = []

    def update_categorie(self):
        if self.comboBox.currentText() == 'https://happygifts.ru/':
            self.categories = HappyGifts().parser_category()
        self.treeWidget.clear()
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
                    if self.comboBox.currentText() == 'https://happygifts.ru/':
                        goods = HappyGifts().parser_goods(categorie['href'])
                        for good in goods:
                            self.goods.append(good)
                            self.listWidget_2.addItem(good['title'] + ' Артикул:' + good['vendor code'])
                else:
                    if categorie['subcategories']:
                        for subcategorie in categorie['subcategories']:
                            if subcategorie['title'] == item.text(0):
                                goods = HappyGifts().parser_goods(subcategorie['href'])
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

    def parsing(self):
        goods = []
        for i in range(0, self.listWidget.count()):
            splited = self.listWidget.item(i).text().split('/')
            main_page = splited[0] + '//' + splited[2] + '/'
            if main_page == 'https://happygifts.ru/':
                good = HappyGifts().parser_good(self.listWidget.item(i).text())
                goods.append([main_page, good])
        wb = xlwt.Workbook()
        sheets_pages = []
        sheets_object = []
        target_row = 1
        for good in goods:
            if good[0] not in sheets_pages:
                sheets_pages.append(good[0])
                sheets_object.append(wb.add_sheet(good[0].split('/')[-2]))
            ws = sheets_object[sheets_pages.index(good[0])]
            if target_row == 1:
                ws.write(target_row, 0, 'Раздел')
                ws.write(target_row, 1, 'Наименование')
                ws.write(target_row, 2, 'Ссылка')
                ws.write(target_row, 3, 'Отметка')
                ws.write(target_row, 4, 'Цена')
                ws.write(target_row, 5, 'Цвет')
                ws.write(target_row, 6, 'Склад 1')
                ws.write(target_row, 7, 'Склад 2')
                ws.write(target_row, 8, 'Склад 3')
                ws.write(target_row, 9, 'Описание')
                ws.write(target_row, 10, 'Материал')
                target_row += 1
            for key, item in good[1].items():
                print(key)
                if key == 'section':
                    ws.write(target_row, 0, str(item))
                elif key == 'name':
                    ws.write(target_row, 1, str(item))
                elif key == 'page':
                    ws.write(target_row, 2, str(item))
                elif key == 'marks':
                    print(item)
                    if item:
                        for i in range(0, len(item)):
                            ws.write(target_row + i, 3, item[i])
                elif key == 'prices':
                    if item:
                        for i in range(0, len(item)):
                            ws.write(target_row + i, 4, item[i])
                elif key == 'colors':
                    if item:
                        for i in range(0, len(item)):
                            ws.write(target_row + i, 5, item[i])
                # доработать(неправильно склады)
                elif key == 'stock_availability':
                    for i in range(0, len(item)):
                        for c in range(0, len(item[i])):
                            ws.write(target_row + i, 6+c, item[i][c])
                elif key == 'descriptions':
                    if item:
                        for i in range(0, len(item)):
                            ws.write(target_row + i, 9, item[i])
                elif key == 'materials':
                    if item:
                        for i in range(0, len(item)):
                            ws.write(target_row + i, 10, item[i])
        wb.save('data.xls')

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
