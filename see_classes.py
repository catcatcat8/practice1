# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/xiaomi/Documents/GitHub/practice1/qt/see_classes.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 540)
        MainWindow.setStyleSheet("background-color: rgb(0, 165, 221);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, -20, 311, 91))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(750, 440, 181, 41))
        self.pushButton_5.setStyleSheet("background-color: rgb(168, 193, 221);\n"
"font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 0, 0);")
        self.pushButton_5.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(440, 340, 491, 41))
        self.pushButton_6.setStyleSheet("background-color: rgb(0, 85, 0);\n"
"color: rgb(255, 255, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_6.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 110, 491, 201))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(70, 70, 331, 401))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">CSS-классы веб-сайта</span></p></body></html>"))
        self.pushButton_5.setText(_translate("MainWindow", "Назад"))
        self.pushButton_6.setText(_translate("MainWindow", "Посмотреть список классов CSS"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">CSS-классы, показанные на данной странице, <br/>используются в CSS файлах верстки <br/>вашего сайта.<br/><br/>!!! Ни в коем случае не удаляйте их <br/>описания в CSS файлах сайта, <br/>это может нарушить работу сайта!!!</span></p></body></html>"))
