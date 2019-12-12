# -*- coding: utf-8 -*-
#import main_window
import main_window_v2
from PyQt5 import QtWidgets
import sys
from parser_happygifts import HappyGifts


class MainApp(QtWidgets.QMainWindow, main_window_v2.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItem('https://happygifts.ru/')
        self.pushButton.clicked.connect(self.update_categorie)
        #self.treeWidget.itemClicked.connect(self.update_goods)
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
                            self.listWidget_2.addItem(good['title']+' Артикул:' + good['vendor code'])
                else:
                    if categorie['subcategories']:
                        for subcategorie in categorie['subcategories']:
                            if subcategorie['title'] == item.text(0):
                                goods = HappyGifts().parser_goods(subcategorie['href'])
                                for good in goods:
                                    self.goods.append(good)
                                    self.listWidget_2.addItem(good['title']+' Артикул:' + good['vendor code'])


    def add_in_outlist(self):
        for select_item in self.listWidget_2.selectedItems():
            for good in self.goods:
                item = good['title']+' Артикул:' + good['vendor code']
                if item == select_item.text():
                    if self.comboBox.currentText() == 'https://happygifts.ru/':
                        self.listWidget.addItem('https://happygifts.ru/' + good['href'][1:])

    def parsing(self):
        for i in range(0,self.listWidget.count()):
            splited = self.listWidget.item(i).text().split('/')
            main_page = splited[0]+'//' + splited[2] + '/'
            if main_page == 'https://happygifts.ru/':
                good = HappyGifts().parser_good(self.listWidget.item(i).text())

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