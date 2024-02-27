import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from untitled import Ui_Form
import second_main
import xlwt  # 负责写excel
import numpy as np
import os

def generateExcel_mstp( list_switch, list_port, list_edge, list_msti):
    list_switch = np.array(list_switch)
    list_port = np.array(list_port)
    list_edge = np.array(list_edge)
    list_msti = np.array(list_msti)
    filename = xlwt.Workbook(encoding = "utf-8")  # 创建工作簿
    sheet_switch = filename.add_sheet(u'switch', cell_overwrite_ok=True)  # 创建sheet
    sheet_port = filename.add_sheet(u'port', cell_overwrite_ok=True)  # 创建sheet
    sheet_edge = filename.add_sheet(u'edge', cell_overwrite_ok=True)  # 创建sheet
    sheet_VLAN = filename.add_sheet(u'VLAN', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = list_switch.shape  # h为行数，l为列数
    for i in range(l):
        sheet_switch.write(0,i," header")
    for i in range(h):
        for j in range(l):
            sheet_switch.write(i + 1, j, list_switch[i, j])
    [h, l] = list_port.shape  # h为行数，l为列数
    for i in range(l):
        sheet_port.write(0, j, " header")
    for i in range(h):
        for j in range(l):
            sheet_port.write(i + 1, j, list_port[i, j])
    [h, l] = list_edge.shape  # h为行数，l为列数
    for i in range(l):
        sheet_edge.write(0, j, " header")
    for i in range(h):
        for j in range(l):
            sheet_edge.write(i + 1, j, list_edge[i, j])

    [h, l] = list_msti.shape  # h为行数，l为列数
    for i in range(l):
        sheet_VLAN.write(0, j, " header")
    for i in range(h):
        for j in range(l):
            sheet_VLAN.write(i + 1, j, list_msti[i, j])
    path = os.path.dirname(os.path.dirname(__file__)) + '/data_test' + '/mstp.xls'
    filename.save(path)  # 保存到当前工作目录
    print(path)

def generateExcel_stp( list_switch, list_port, list_edge):
    list_switch = np.array(list_switch)
    list_port = np.array(list_port)
    list_edge = np.array(list_edge)
    filename = xlwt.Workbook(encoding = "utf-8")  # 创建工作簿
    sheet_switch = filename.add_sheet(u'switch', cell_overwrite_ok=True)  # 创建sheet
    sheet_port = filename.add_sheet(u'port', cell_overwrite_ok=True)  # 创建sheet
    sheet_edge = filename.add_sheet(u'edge', cell_overwrite_ok=True)  # 创建sheet
    [h, l] = list_switch.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet_switch.write(i + 1, j, list_switch[i, j])
    [h, l] = list_port.shape  # h为行数，l为列数
    for i in range(h):
        for j in range(l):
            sheet_port.write(i + 1, j, list_port[i, j])
    [h, l] = list_edge.shape  # h为行数，l为列数
    for i in range(h ):
        for j in range(l):
            sheet_edge.write(i + 1, j, list_edge[i, j])
    path = os.path.dirname(os.path.dirname(__file__)) + '/data_test' + '/stp.xls'
    filename.save(path)  # 保存到当前工作目录
    print(path)


class Demo(QWidget, Ui_Form):
    def __init__(self):
        super(Demo, self).__init__()
        self.setupUi(self)
        #STP按钮和MSTP按钮, 按下按钮会获得当前的输入文件
        self.pushButton.clicked.connect(self.mstp_start)
        self.pushButton_2.clicked.connect(self.stp_start)
        self.pushButton_3.clicked.connect(self.stp_data)
        self.pushButton_4.clicked.connect(self.mstp_data)
        self.pushButton_5.clicked.connect(self.open_btn_clicked)

    def open_btn_clicked(self):
        """点击相应按钮，跳转到第二个界面"""
        # 实例化第二个界面的后端类，并对第二个界面进行显示
        # 通过派生新类去访问类
        self.another_window = second_main.AnotherWindowActions()
        second_main.show1(self.another_window)
        self.another_window.show()



    def mstp_start(self):
        fp = self.lineEdit.text()
        print('文件输入 mstp开始')
        print(fp)

    def stp_start(self):
        print('文件输入 stp开始')
        fp = self.lineEdit.text()
        print(fp)





    def stp_data(self):
        list_switch = list()
        list_port = list()
        list_edge = list()
        #对于Switch子表来说

        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        for i in range(rows) :
            if self.tableWidget.item(i, 0) is None:
                break
            list_switch.append(list())
            for j in range(cols):

                data = self.tableWidget.item(i, j).text()
                if data == 'none' :
                    continue
                else:
                    list_switch[i].append(data)

        rows = self.tableWidget_2.rowCount()
        cols = self.tableWidget_2.columnCount()
        for i in range(rows):
            if self.tableWidget_2.item(i, 0) is None:
                break
            list_port.append(list())
            for j in range(cols):

                data = self.tableWidget_2.item(i, j).text()
                if data == 'none':
                    continue
                else:
                    list_port[i].append(data)



        rows = self.tableWidget_3.rowCount()
        cols = self.tableWidget_3.columnCount()
        for i in range(rows):
            if self.tableWidget_3.item(i, 0) is None:
                break
            list_edge.append(list())
            for j in range(cols):
                data = self.tableWidget_3.item(i, j).text()
                if data == 'none':
                    continue
                else:
                    list_edge[i].append(data)
        print(list_switch)
        print(list_port)
        print(list_edge)
        generateExcel_stp(list_switch, list_port, list_edge)
        with open('run.py', 'r') as f:
            exec(f.read())


    def mstp_data(self):
        list_switch = list()
        list_port = list()
        list_edge = list()
        list_msti = list()
        # 对于Switch子表来说

        rows = self.tableWidget_4.rowCount()
        cols = self.tableWidget_4.columnCount()
        for i in range(rows):
            if self.tableWidget_4.item(i, 0) is None:
                break
            list_switch.append(list())
            for j in range(cols):

                data = self.tableWidget_4.item(i, j).text()
                if data is None:
                    continue
                else:
                    list_switch[i].append(data)

        rows = self.tableWidget_5.rowCount()
        cols = self.tableWidget_5.columnCount()
        for i in range(rows):
            if self.tableWidget_5.item(i, 0) is None:
                break
            list_port.append(list())
            for j in range(cols):

                data = self.tableWidget_5.item(i, j).text()
                if data == 'none':
                    continue
                else:
                    list_port[i].append(data)

        rows = self.tableWidget_6.rowCount()
        cols = self.tableWidget_6.columnCount()
        for i in range(rows):
            if self.tableWidget_6.item(i, 0) is None:
                break
            list_edge.append(list())
            for j in range(cols):
                data = self.tableWidget_6.item(i, j).text()
                if data == 'none':
                    continue
                else:
                    list_edge[i].append(data)

        rows = self.tableWidget_7.rowCount()
        cols = self.tableWidget_7.columnCount()
        for i in range(rows):
            if self.tableWidget_7.item(i, 0) is None:
                break
            list_msti.append(list())
            for j in range(cols):

                data = self.tableWidget_7.item(i, j).text()
                if data == 'none':
                    continue
                else:
                    list_msti[i].append(data)
        print(list_switch)
        print(list_port)
        print(list_edge)
        print(list_msti)
        generateExcel_mstp(list_switch, list_port, list_edge, list_msti)
        ##调用程序
        with open('run.py', 'r') as f:
            exec(f.read())


## 表格创建函数






if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec())