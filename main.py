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
        self.pushButton_2.clicked.connect(self.save_excel)
        self.treeWidget.itemClicked.connect(self.update_goods)
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
                            self.listWidget_2.addItem(good['title'])
                else:
                    if categorie['subcategories']:
                        for subcategorie in categorie['subcategories']:
                            if subcategorie['title'] == item.text(0):
                                goods = HappyGifts().parser_goods(subcategorie['href'])
                                for good in goods:
                                    self.goods.append(good)
                                    self.listWidget_2.addItem(good['title'])

    def save_excel(self):
        for item in self.listWidget_2.selectedItems():
            for good in self.goods:
                if good['title'] == item.text():
                    HappyGifts().parser_good(good['href'])



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()