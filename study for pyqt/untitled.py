# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(647, 357)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 50, 641, 261))
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(60, 80, 541, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 130, 541, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 10, 171, 61))
        self.label.setStyleSheet("font: 25pt \".AppleSystemUIFont\";")
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 0, 631, 231))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setToolTip("")
        self.tab_4.setObjectName("tab_4")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget.setGeometry(QtCore.QRect(140, 0, 311, 201))
        self.tableWidget.setRowCount(20)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_2.setGeometry(QtCore.QRect(130, 10, 341, 201))
        self.tableWidget_2.setRowCount(40)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget_3.setGeometry(QtCore.QRect(160, 0, 311, 201))
        self.tableWidget_3.setRowCount(20)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        self.tableWidget_3.verticalHeader().setVisible(False)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_3.setGeometry(QtCore.QRect(490, 135, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget_2.addTab(self.tab_6, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.tab_3)
        self.tabWidget_3.setGeometry(QtCore.QRect(4, 0, 631, 241))
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_7)
        self.tableWidget_4.setGeometry(QtCore.QRect(60, 0, 511, 201))
        self.tableWidget_4.setRowCount(20)
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.tableWidget_4.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_4.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_4.setHorizontalHeaderItem(4, item)
        self.tableWidget_4.verticalHeader().setVisible(False)
        self.tabWidget_3.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.tableWidget_5 = QtWidgets.QTableWidget(self.tab_8)
        self.tableWidget_5.setGeometry(QtCore.QRect(100, 0, 411, 211))
        self.tableWidget_5.setRowCount(40)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(3, item)
        self.tableWidget_5.verticalHeader().setVisible(False)
        self.tabWidget_3.addTab(self.tab_8, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.tableWidget_6 = QtWidgets.QTableWidget(self.tab_10)
        self.tableWidget_6.setGeometry(QtCore.QRect(160, 0, 311, 211))
        self.tableWidget_6.setRowCount(30)
        self.tableWidget_6.setObjectName("tableWidget_6")
        self.tableWidget_6.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_6.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_6.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_6.setHorizontalHeaderItem(2, item)
        self.tableWidget_6.verticalHeader().setVisible(False)
        self.tabWidget_3.addTab(self.tab_10, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.tableWidget_7 = QtWidgets.QTableWidget(self.tab_9)
        self.tableWidget_7.setGeometry(QtCore.QRect(110, 0, 411, 211))
        self.tableWidget_7.setRowCount(20)
        self.tableWidget_7.setObjectName("tableWidget_7")
        self.tableWidget_7.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_7.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_7.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_7.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_7.setHorizontalHeaderItem(3, item)
        self.tableWidget_7.verticalHeader().setVisible(False)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_9)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 160, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget_3.addTab(self.tab_9, "")
        self.tabWidget.addTab(self.tab_3, "")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 15, 531, 21))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(30, 10, 301, 21))
        self.label_3.setStyleSheet("font: 20pt \".AppleSystemUIFont\";")
        self.label_3.setObjectName("label_3")
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(540, 320, 101, 31))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(2)
        self.tabWidget_3.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit.setPlaceholderText(_translate("Form", "请输入文件路径"))
        self.pushButton_2.setText(_translate("Form", "STP"))
        self.pushButton.setText(_translate("Form", "MSTP"))
        self.label.setText(_translate("Form", "文件路径："))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "文件输入"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Port"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "BID"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Name"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("Form", "Switch子表"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "PID"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "SPID"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Form", "Port_子表"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Port1"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Port2"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Cost"))
        self.pushButton_3.setText(_translate("Form", "输入完成"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("Form", "Edge子表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "STP_algorithm"))
        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Port"))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Priority"))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("Form", "mac"))
        item = self.tableWidget_4.horizontalHeaderItem(3)
        item.setText(_translate("Form", "name"))
        item = self.tableWidget_4.horizontalHeaderItem(4)
        item.setText(_translate("Form", "region_name"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_7), _translate("Form", "Switch子表"))
        item = self.tableWidget_5.horizontalHeaderItem(0)
        item.setText(_translate("Form", "PortID"))
        item = self.tableWidget_5.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Port"))
        item = self.tableWidget_5.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Priority"))
        item = self.tableWidget_5.horizontalHeaderItem(3)
        item.setText(_translate("Form", "VLAN"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_8), _translate("Form", "Port子表"))
        item = self.tableWidget_6.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Port1"))
        item = self.tableWidget_6.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Port2"))
        item = self.tableWidget_6.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Cost"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_10), _translate("Form", "Edge子表"))
        item = self.tableWidget_7.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Region_name"))
        item = self.tableWidget_7.horizontalHeaderItem(1)
        item.setText(_translate("Form", "MSTI_ID"))
        item = self.tableWidget_7.horizontalHeaderItem(2)
        item.setText(_translate("Form", "VLAN_ID"))
        item = self.tableWidget_7.horizontalHeaderItem(3)
        item.setText(_translate("Form", "RootBridge"))
        self.pushButton_4.setText(_translate("Form", "输入完成"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_9), _translate("Form", "MSTI_VLAN映射表"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "MSTP/RSTP_algorithm"))
        self.label_3.setText(_translate("Form", "网络二层协议仿真工具"))
        self.pushButton_5.setText(_translate("Form", "详细信息"))
