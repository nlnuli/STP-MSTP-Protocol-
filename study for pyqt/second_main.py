import sys
import second
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox,QLabel
from PyQt5 import QtWidgets
import numpy as np
from PyQt5.QtGui import QPixmap


def show1(x):
    pix = QPixmap(r'1.png')


    x.label_5.setPixmap(pix)
    x.label_5.setScaledContents(True)

    file = open('print.txt', 'r', encoding='utf-8')
    data = file.readlines()
    for i in range(len(data)):
        x.textBrowser.append(data[i])

    file.close()


# 业务类需要继承两个类，一个设计的主界面，另一个是QMainWindow
class AnotherWindowActions(second.Ui_Form_2, QMainWindow):
    def __init__(self):
        """
         特别注意（最容易出错）：
         1.派生新类访问基类需要super(),同时它的参数是基类文件下的类及“ui_home_window.py中的
           Ui_MainWindow类”，
        """
        super(second.Ui_Form_2, self).__init__()
        self.setupUi(self)





