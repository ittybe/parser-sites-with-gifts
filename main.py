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
        self.pushButton.clicked.connect(self.update_category)

    def update_category(self):
        if self.comboBox.currentText() == 'https://happygifts.ru/':
            categories = HappyGifts().parser_category()
            print(categories)
            if self.listWidget.count()>1:
                for i in range(0,self.listWidget.count()):
                    self.listWidget.removeItemWidget(self.listWidget.item(i))
            for categorie in categories:
                item = QtWidgets.QListWidgetItem()
                item.setText(categorie)
                self.listWidget.addItem(item)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()