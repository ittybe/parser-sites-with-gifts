#!/usr/bin/python3
# -*- coding: utf-8 -*-
# import main_window
import main_window_v2
import dialog_window
from PyQt5 import QtWidgets
import sys
from parser_happygifts import HappyGifts
from parser_gifts import Gifts
from parser_oasiscatalog import Oasiscatalog
import xlwt
import time
from PyQt5.QtCore import QThread
import datetime
import os
import json
import xlrd
from xlutils.copy import copy
### Сделать так что бы виджеты были привязаны к combobox только один раз
class MainApp(QtWidgets.QMainWindow, main_window_v2.Ui_MainWindow):
    days_weekly = {
        'Понедельник':  0,
        'Вторник': 1,
        'Среда': 2,
        'Четверг': 3,
        'Пятница': 4,
        'Суббота': 5,
        'Воскресенье': 6,
    }
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
        self.listWidget_3.itemClicked.connect(self.remove_href)
        self.pushButton_5.clicked.connect(self.update_goods)
        self.pushButton_2.clicked.connect(self.add_in_outlist)
        self.pushButton_3.clicked.connect(lambda :self.parsing(self.get_goods()))
        self.pushButton_6.clicked.connect(self.add_page)
        self.pushButton_4.clicked.connect(self.open_dialog)
        self.categories = []
        self.goods = []
        self.timedata = []
        self.timer = TimerRun(self)
        self.open_json()



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
                        self.listWidget_3.addItem('https://happygifts.ru/' + good['href'][1:])
                    elif self.comboBox.currentText() == 'https://gifts.ru/':
                        self.listWidget.addItem('https://gifts.ru/' + good['href'][1:])
                        self.listWidget_3.addItem('https://gifts.ru/' + good['href'][1:])
                    elif self.comboBox.currentText() == 'https://www.oasiscatalog.com/':
                        self.listWidget.addItem('https://www.oasiscatalog.com/' + good['href'][1:])
                        self.listWidget_3.addItem('https://gifts.ru/' + good['href'][1:])

    def get_goods(self):
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
        return goods

    def parsing(self, goods):
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

    def add_page(self):
        item = self.lineEdit.text()
        self.listWidget.addItem(item)

    def remove_href(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
        for item in self.listWidget_3.selectedItems():
            self.listWidget_3.takeItem(self.listWidget_3.row(item))

    def open_dialog(self):
        if self.pushButton_4.isChecked():
            dialog = Dialog()
            dialog.exec_()
            if dialog.accepted:
                get_time = dialog.time.split(':')
                self.timedata = [self.days_weekly[dialog.day],
                                 datetime.time(hour=int(get_time[0]),
                                               minute=int(get_time[1])),
                                 int(dialog.count_pars),
                                 0]
                if self.timedata[2]>0:
                    self.timer.timedata = self.timedata
                    self.timer.start()
                    self.pushButton_4.setText('Остановиь парсинг')
                    self.save_json()
                else:
                    self.pushButton_4.setChecked(False)
                    self.pushButton_4.setText('Парсинг')
            else:
                self.pushButton_4.setChecked(False)
                self.timer.timedata[2] = 0
                self.pushButton_4.setText('Парсинг')
        else:
            self.pushButton_4.setText('Парсинг')
            self.timer.timedata[2] = 0

    def parsing_time(self):
        goods = []
        for i in range(0, self.listWidget_3.count()):
            splited = self.listWidget_3.item(i).text().split('/')
            main_page = splited[0] + '//' + splited[2] + '/'
            if main_page == 'https://happygifts.ru/':
                good = self.happygifts.parser_good(self.listWidget_3.item(i).text())
                goods.append([main_page, good])
                print(good)
            elif main_page == 'https://gifts.ru/':
                good = self.gifts.parser_good(self.listWidget_3.item(i).text())
                goods.append([main_page, good])
                print(good)
            elif main_page == 'https://www.oasiscatalog.com/':
                good = self.oasiscatalog.parser_good(self.listWidget_3.item(i).text())
                goods.append([main_page, good])
                print(good)
        if goods:
            count_pars = self.timer.timedata[3]
            if count_pars == 0:
                wb = xlwt.Workbook()
                ws = wb.add_sheet('parsing', cell_overwrite_ok = True)
                ws.write(count_pars, 0, 'Наименование')
                ws.write(count_pars, 1, 'Ссылка')
                ws.write(count_pars, 2, 'Цвет')
                tr = 1
                for good in goods:
                    for key, item in good[1].items():
                        if key == 'name':
                            ws.write(tr, 0, str(item))
                        elif key == 'page':
                            ws.write(tr, 1, str(item))
                        elif key == 'colors':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, 2, item[i])
                    tr += len(good[1]['colors'])
                    wb.save('data_timing.xls')
            rb = xlrd.open_workbook('data_timing.xls', on_demand=True, formatting_info=True)
            wb = copy(rb)
            rb.release_resources()
            ws = wb.get_sheet(0)
            tr = 1
            now = datetime.datetime.now()
            ws.write(0, count_pars+3,str(now))
            for good in goods:
                for key, item in good[1].items():
                    if key == 'stock_availability':
                        if good[0] == 'https://happygifts.ru/':
                            if item:
                                for i in range(0, len(item)):
                                    all_stocks = sum([number for name, number in item[i].items()])
                                    ws.write(tr + i, count_pars + 3, all_stocks)
                        if good[0] == 'https://gifts.ru/':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, count_pars+3, item[i])
                        if good[0] == 'https://www.oasiscatalog.com/':
                            if item:
                                for i in range(0, len(item)):
                                    ws.write(tr + i, count_pars+3, item[i])
                tr += len(good[1]['colors'])
            wb.save('data_timing.xls')








    def save_json(self):
        try:
            timedata = [self.timer.timedata[0],
                        str(self.timer.timedata[1]),
                        self.timer.timedata[2],
                        self.timer.timedata[3]]
            to_json = {'timedata': timedata,
                    'pages': [self.listWidget_3.item(i).text() for i in range(0, self.listWidget_3.count())]}
            with open('timedata.json', 'w') as f:
                json.dump(to_json, f)
        except Exception as ex:
            print(ex)

    def open_json(self):
        if os.path.exists('timedata.json'):
            with open('timedata.json') as f:
                timedata_file = json.load(f)
                if timedata_file['timedata'][2]>0:
                    print('ok')
                    for page in timedata_file['pages']:
                        self.listWidget_3.addItem(page)
                    get_time = timedata_file['timedata'][1].split(':')
                    self.timer.timedata = [timedata_file['timedata'][0],
                                            datetime.time(hour=int(get_time[0]), minute=int(get_time[1])),
                                            timedata_file['timedata'][2],
                                           timedata_file['timedata'][3]]
                    self.timer.start()
                    self.pushButton_4.setText('Остановиь парсинг')
                    self.pushButton_4.setChecked(True)






class Dialog(QtWidgets.QDialog, dialog_window.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.cancel)
        self.comboBox.addItem('Понедельник')
        self.comboBox.addItem('Вторник')
        self.comboBox.addItem('Среда')
        self.comboBox.addItem('Четверг')
        self.comboBox.addItem('Пятница')
        self.comboBox.addItem('Суббота')
        self.comboBox.addItem('Воскресенье')
        self.accepted = False
        self.day = None
        self.time = None
        self.count_pars = None

    def accept(self):
        self.day = self.comboBox.currentText()
        self.time = self.timeEdit.text()
        self.count_pars = self.spinBox_2.text()
        self.accepted = True
        self.close()

    def cancel(self):
        self.accepted = False
        self.close()


class TimerRun(QThread):
    def __init__(self, mainWindow):
        super().__init__()
        self.value = 0
        self.mainWindow = mainWindow
        self.timedata = []
        self.parsed = []

    def run(self):
        while True:
            if self.timedata[2]>0:
                time.sleep(1)
                now = datetime.datetime.now()
                if now.weekday() == self.timedata[0]\
                        and now.time().minute == self.timedata[1].minute \
                        and now.time().hour == self.timedata[1].hour:
                    if [now.day, now.time().hour, now.time().minute] not in self.parsed:
                        print('[INFO] PARSING...')
                        self.mainWindow.parsing_time()
                        self.parsed.append([now.day, now.time().hour, now.time().minute])
                        print('[INFO] complete')
                        self.timedata[2] -= 1
                        self.timedata[3] += 1
                        self.mainWindow.save_json()
            else:
                self.mainWindow.pushButton_4.setChecked(False)
                self.mainWindow.pushButton_4.setText('Парсинг')
                self.mainWindow.save_json()
                break


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
