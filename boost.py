# Лебедев Евгений: Интерфейс программы ускорения работы веб-сайтов
import sys
import mainpage
import reference
import mainmenu
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

width = 1920
height = 1080

class ExampleApp(QtWidgets.QMainWindow, mainpage.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # инициализация нашего дизайна
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.menu)
        self.pushButton_3.clicked.connect(self.about)
    
    def closeEvent(self, event):
 
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def about(self):
        self.about_form = ReferenceApp()
        self.about_form.show()

    def menu(self):
        self.menu_form = MenuApp()
        self.menu_form.show()

class MenuApp(QtWidgets.QMainWindow, mainmenu.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма меню
        self.setWindowTitle('Меню')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton_5.clicked.connect(self.close)

class ReferenceApp(QtWidgets.QMainWindow, reference.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма справки
        self.setWindowTitle('Справка')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton.clicked.connect(self.close)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()