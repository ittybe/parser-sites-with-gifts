# -*- coding: utf-8 -*-
import main_window
from PyQt5 import QtWidgets
import sys
from parser_happygifts import HappyGifts


class MainApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItem('https://happygifts.ru/')
        self.pushButton.clicked.connect(self.update_categorie)
        self.listWidget.itemClicked.connect(self.update_subcategorie)
        self.listWidget_3.itemClicked.connect(self.update_goods)
        self.categories = []
        self.goods = []

    def update_categorie(self):
        if self.comboBox.currentText() == 'https://happygifts.ru/':
            self.categories = HappyGifts().parser_category()
            print(self.categories)
            if self.listWidget.count() > 0:
                self.listWidget.clear()
            for categorie in self.categories:
                item = QtWidgets.QListWidgetItem()
                item.setText(categorie['title'])
                self.listWidget.addItem(item)

    def update_subcategorie(self):
        if self.listWidget_3.count() > 0:
            self.listWidget_3.clear()
        for item in self.listWidget.selectedItems():
            it = QtWidgets.QListWidgetItem()
            it.setText(item.text())
            self.listWidget_3.addItem(it)

    def update_goods(self):
        if self.listWidget_2.count() > 0:
            self.listWidget_2.clear()
            self.goods = []
        for item in self.listWidget_3.selectedItems():
            for categorie in self.categories:
                if categorie['title'] == item.text():
                    if self.comboBox.currentText() == 'https://happygifts.ru/':
                        goods = HappyGifts().parser_goods(categorie['href'])
                        for good in goods:
                            self.goods.append(good)
                            self.listWidget_2.addItem(good['title'])
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()