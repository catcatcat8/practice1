# Лебедев Евгений: Программа ускорения работы веб-сайтов
import sys
from forms import mainpage, reference, mainmenu, see_tags, see_classes, see_ids, see_boost
import logic
import pyqtgraph as pg 
from pyqtgraph import PlotWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QFileDialog, QErrorMessage, QSizePolicy, QVBoxLayout, QDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

width = 1920
height = 1080

html_path = ''
css_path = ''
statistics = ''
count_css_processed = []
optimized_base = []
optimized_opt = []

class ExampleApp(QtWidgets.QMainWindow, mainpage.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # инициализация нашего дизайна
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.menu)
        self.pushButton_3.clicked.connect(self.about)
    
    def closeEvent(self, event):
 
        reply = QMessageBox.question(self, 'Quit',
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
        self.pushButton.clicked.connect(self.show_boost)
        self.pushButton_2.clicked.connect(self.show_tags)
        self.pushButton_3.clicked.connect(self.show_classes)
        self.pushButton_4.clicked.connect(self.show_ids)
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.choose_html_files)
        self.pushButton_7.clicked.connect(self.choose_css_files)

    def show_boost(self):
        global html_path, css_path
        if (html_path != '' and css_path != ''):
            self.boost_form = SeeBoostApp()
            self.boost_form.show()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Сначала выберите HTML и CSS файлы сайта!")
            msg.setWindowTitle("Error")
            msg.exec_()
    
    def show_tags(self):
        global html_path, css_path
        if (html_path != '' and css_path != ''):
            self.tags_form = SeeTagsApp()
            self.tags_form.show()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Сначала выберите HTML и CSS файлы сайта!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def show_classes(self):
        global html_path, css_path
        if (html_path != '' and css_path != ''):
            self.classes_form = SeeClassesApp()
            self.classes_form.show()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Сначала выберите HTML и CSS файлы сайта!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def show_ids(self):
        global html_path, css_path
        if (html_path != '' and css_path != ''):
            self.id_form = SeeIdsApp()
            self.id_form.show()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Сначала выберите HTML и CSS файлы сайта!")
            msg.setWindowTitle("Error")
            msg.exec_()

    def choose_html_files(self):
        html_dir = QFileDialog.getExistingDirectory(self, 'Выберите директорию с HTML файлами сайта')
        if html_dir:
            global html_path 
            html_path = html_dir
            self.pushButton_6.setStyleSheet("background-color: rgb(0, 85, 0);\n"
            "font: 10pt \"MS Shell Dlg 2\";\n"
            "color: rgb(255, 255, 255);")

    def choose_css_files(self):
        css_dir = QFileDialog.getExistingDirectory(self, 'Выберите директорию с CSS файлами сайта')
        if css_dir:
            global css_path
            css_path = css_dir
            self.pushButton_7.setStyleSheet("background-color: rgb(0, 85, 0);\n"
            "font: 10pt \"MS Shell Dlg 2\";\n"
            "color: rgb(255, 255, 255);")
            

class ReferenceApp(QtWidgets.QMainWindow, reference.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма справки
        self.setWindowTitle('Справка')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton.clicked.connect(self.close)

class SeeTagsApp(QtWidgets.QMainWindow, see_tags.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма тегов
        self.setWindowTitle('Используемые теги')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.calculate_tags)

    def calculate_tags(self):
        all_tags = []
        all_html_docs, all_css_docs = logic.html_css_existence(html_path, css_path)
        if all_html_docs:
            for each_html_doc in all_html_docs:
                cur_file_enc = logic.my_encoding(each_html_doc)
                # Получение списка тегов из всех html документов
                all_used_tags, err_event = logic.html_tags(each_html_doc, cur_file_enc)
                for each_tag in all_used_tags:
                    if each_tag and each_tag not in all_tags:
                        all_tags.append(each_tag)
        resultstr = ''
        all_tags = sorted(list(set(all_tags)))
        if all_tags:
            for tag in all_tags:
                resultstr += tag.upper() + '\n'
            self.textBrowser.setText(resultstr)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не найдено ни одного HTML-тега!")
            msg.setInformativeText('Проверьте правильность выбора HTML/CSS файлов сайта...')
            msg.setWindowTitle("Error")
            msg.exec_()

class SeeClassesApp(QtWidgets.QMainWindow, see_classes.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма тегов
        self.setWindowTitle('Используемые CSS-классы')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.calculate_classes)

    def calculate_classes(self):
        all_classes = []
        all_html_docs, all_css_docs = logic.html_css_existence(html_path, css_path)
        if all_html_docs:
            for each_html_doc in all_html_docs:
                cur_file_enc = logic.my_encoding(each_html_doc)
                # Получение списка CSS классов
                all_used_classes = logic.class_list(each_html_doc, cur_file_enc)  # список классов
                for each_class in all_used_classes:
                    if each_class and each_class not in all_classes:
                        all_classes.append(each_class)
        resultstr = ''
        all_classes = sorted(list(set(all_classes)))
        if all_classes:
            for cur_class in all_classes:
                resultstr += cur_class + '\n'
            self.textBrowser.setText(resultstr)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не найдено ни одного CSS-класса")
            msg.setWindowTitle("Error")
            msg.exec_()

class SeeIdsApp(QtWidgets.QMainWindow, see_ids.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма тегов
        self.setWindowTitle('Используемые CSS-идентификаторы')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.calculate_ids)

    def calculate_ids(self):
        all_ids = []
        all_html_docs, all_css_docs = logic.html_css_existence(html_path, css_path)
        if all_html_docs:
            for each_html_doc in all_html_docs:
                cur_file_enc = logic.my_encoding(each_html_doc)
                # Получение списка CSS идентификаторов
                all_used_ids = logic.id_list(each_html_doc, cur_file_enc)  # список идентификаторов
                for each_id in all_used_ids:
                    if each_id and each_id not in all_ids:
                        all_ids.append(each_id)
        resultstr = ''
        all_ids = sorted(list(set(all_ids)))
        if all_ids:
            for cur_id in all_ids:
                resultstr += cur_id + '\n'
            self.textBrowser.setText(resultstr)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Не найдено ни одного CSS-идентификатора")
            msg.setWindowTitle("Error")
            msg.exec_()

class SeeBoostApp(QtWidgets.QMainWindow, see_boost.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # форма тегов
        self.setWindowTitle('Ускорение работы веб-сайта')
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton_5.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.boosting)
           
        

    def boosting(self):
        self.textBrowser.setText("")
        _tmp = "Проверьте правильность выбора HTML/CSS файлов"
        report_file = open("report.txt", "w", encoding="utf-8")  # создание файла с информацией о работе скрипта
        all_html_docs, all_css_docs = logic.html_css_existence(html_path, css_path)
        if all_html_docs and all_css_docs:  # если передали хотя бы 1 html файл и хотя бы 1 css файл
            all_tags = []
            all_styles = []
            all_classes = []
            all_ids = []
            for each_html_doc in all_html_docs:
                all_used_tags = []
                styles = []
                all_used_classes = []
                all_used_ids = []
                cur_file_enc = logic.my_encoding(each_html_doc)  # определяем кодировку файла
                # --- Шаг 1
                # Получение списка тегов из всех html документов
                all_used_tags, err_event = logic.html_tags(each_html_doc, cur_file_enc)
                for each_tag in all_used_tags:
                    if each_tag and each_tag not in all_tags:
                        all_tags.append(each_tag)
                # --- Шаг 2
                # Получение списка всех подгружаемых каскадных таблиц
                styles, err_event = logic.css_styles(each_html_doc, cur_file_enc)
                for each_style in styles:
                    if each_style and each_style not in all_styles:
                        all_styles.append(each_style)
                # --- Шаг 3
                # Получение списка классов и идентификаторов
                all_used_classes = logic.class_list(each_html_doc, cur_file_enc)  # список классов
                for each_class in all_used_classes:
                    if each_class and each_class not in all_classes:
                        all_classes.append(each_class)
                all_used_ids = logic.id_list(each_html_doc, cur_file_enc)  # список идентификаторов
                for each_id in all_used_ids:
                    if each_id and each_id not in all_ids:
                        all_ids.append(each_id)
            # получен список тегов
            report_file.write("---HTML tags---\n")
            [report_file.write(f'{x.upper()}\n') for x in all_tags]
            # получен список локальных стилей
            report_file.write("\n---Local CSS styles---")
            [report_file.write(f'\n{x} ') for x in all_styles]
            # получен список идентификаторов
            report_file.write("\n\n---Id list---")
            [report_file.write(f'\n{x} ') for x in all_ids]
            # получен список используемых классов
            report_file.write("\n\n---Class list---")
            [report_file.write(f'\n{x} ') for x in all_classes]
            # --- Шаг 4
            # Обработка CSS документов
            css_docs = []
            for css_doc in all_styles:
                flag_file_found = False
                for real_css_doc in all_css_docs:
                    if css_doc in real_css_doc:
                        flag_file_found = True
                        cur_file_enc = logic.my_encoding(real_css_doc)
                        css_docs.append(logic.css_work(real_css_doc, cur_file_enc, all_tags, all_classes, all_ids))
                        break
                if not flag_file_found:
                    self.textBrowser.append(f'Файл {css_doc} не был обработан, т.к. не находится в указанной директории')
                    report_file.write(f'Файл {css_doc} не был обработан, т.к. не находится в указанной директории\n')
            global count_css_processed
            count_css_processed = logic.count_css_processed
            n = []
            for each_css in count_css_processed:
                if each_css not in n:
                    n.append(each_css)
            count_css_processed = n

            # --- Шаг 5
            # Создание минимизированных файлов
            dict_num = 0
            for css_doc in all_styles:
                for real_css_doc in all_css_docs:
                    if css_doc in real_css_doc:
                        cur_file_enc = logic.my_encoding(real_css_doc)
                        logic.new_css(real_css_doc, cur_file_enc, css_docs[dict_num])  # создаются минимизированные файлы css
                        dict_num += 1
                        break
            for each_html_doc in all_html_docs:
                cur_file_enc = logic.my_encoding(each_html_doc)
                logic.new_html(each_html_doc, cur_file_enc, all_styles)  # создается новый html файл
            # Вывод названия обработанных файлов
            self.textBrowser.append(f'Обработано {len(count_css_processed)} CSS файла:')
            [self.textBrowser.append(x) for x in count_css_processed]
            report_file.write(f'\n\nОбработано {len(count_css_processed)} CSS файла:\n')
            [report_file.write(f'{x}\n') for x in count_css_processed]
            logic.stats(count_css_processed)
            global statistics
            statistics = logic.stats_text
            self.textBrowser.append(statistics)
            self.pushButton_6.setStyleSheet("background-color: rgb(0, 85, 0);\n"
            "font: 10pt \"MS Shell Dlg 2\";\n"
            "color: rgb(255, 255, 255);")

            global optimized_base, optimized_opt
            optimized_base = logic.optimized_base
            optimized_opt = logic.optimized_opt

            xx = range(len(optimized_base))
            new_x = []
            for i in xx:
                new_x.append(i+1)
            xx = new_x
            self.graphicsView.addLegend(offset=(100, 30))
            self.graphicsView.setXRange(1, len(optimized_base))

            self.graphicsView.plot(xx, optimized_base, pen='r', symbol ='x', 
            symbolPen = 'r', symbolBrush = 0.1, name ='Исходные файлы')
            self.graphicsView.plot(xx, optimized_opt, pen='g', symbol ='o',
            symbolPen = 'g', symbolBrush = 0.1, name = 'Оптимизированные файлы')

            self.graphicsView.setLabel('left', 'Размер файлов', units ='kbytes')
            self.graphicsView.setLabel('bottom', 'Номер файла')
            self.graphicsView.showGrid(x = True, y = True)
            
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(_tmp)
            msg.setWindowTitle("Error")
            msg.exec_()
            report_file.write(_tmp)
        report_file.close()

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()