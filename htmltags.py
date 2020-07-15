# Лебедев Евгений Получение оптимизационного файла (минимизация структуры подгружаемых каскадных таблиц в HTML)
import os
import sys
import re
from chardet.universaldetector import UniversalDetector

class Htmlobject:
    """Класс, описывающий объект HTML"""

    def __init__ (self, tag_name, class_names):  # инициализация
        self.tag_name = tag_name
        self.class_names = class_names

    def htmlobject_print(self):
        print(f'\nТег: {self.tag_name}\nИспользуемые классы CSS: {self.class_names}')  # вывод информации об объекте

def html_css_existence(html_path, css_path):
    """Возвращает все файлы html и css переданные в run.bad"""

    all_html_docs = []
    all_css_docs = []
    if html_path.split('\\')[-1].find('.htm') != -1:
        only_path = html_path[:html_path.rfind('\\')+1]
        only_file = html_path[html_path.rfind('\\')+1:]
        if os.path.exists(only_path):
            listFiles = os.listdir(only_path)
            if only_file in listFiles:
                all_html_docs.append(only_path+only_file)
        else: 
            print('Html файл не найден!')
    else:
        if os.path.exists(html_path):
            listFiles = os.listdir(html_path)
            all_html_docs = ([f'{html_path}\\' + x for x in listFiles if (x.split(".")[-1] in ["html", "htm"] and x.split(".")[-2][0] not in ["_"])])
        else:
            print('Директория с файлами html не найдена!')
    if all_html_docs:  # если список переданных html файлов не пустой проверяем css
        if css_path.split('\\')[-1].find('.css') != -1:
            only_path = css_path[:css_path.rfind('\\')+1]
            only_file = css_path[css_path.rfind('\\')+1:]
            if os.path.exists(only_path):
                listFiles = os.listdir(only_path)
                if only_file in listFiles:
                    all_css_docs.append(only_path+only_file)
            else: 
                print('CSS файл не найден!')
        else:
            if os.path.exists(css_path):
                listFiles = os.listdir(css_path)
                all_css_docs = ([f'{css_path}\\' + x for x in listFiles if (x.split(".")[-1] in ['css'] and x.split(".")[-2][0] not in ["_"])])
            else:
                print('Директория с файлами css не найдена!')
    return all_html_docs, all_css_docs

def encoding(file_path):
    """Вернуть кодировку файла"""

    detector = UniversalDetector()
    with open(file_path, 'rb') as f:
        for line in f:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    cur_file_enc = detector.result['encoding']
    return cur_file_enc

def html_tags(file_path, cur_file_enc):
    """Вернуть список тегов"""

    err_event = None  # возвращаемый текст ошибки
    tags = []  # возвращаемый список переменных
    if file_path is not None:
        with open (file_path, encoding=f'{cur_file_enc}') as f:
            for line in f:
                while (line.find('<') != -1) and (line.find('<!--') == -1):
                    line = line[line.find('<'):]
                    split_lines = line.split()
                    first_tag = split_lines[0].split('>')
                    tag = first_tag[0]
                    # проверка на открывающий и уникальный тег
                    if (tag[0] == '<') and (tag[1].isalpha()) and (tag[1:] not in tags):
                        tags.append(tag[1:])
                    line = line[line.find(f'{tag}')+len(tag)+1:]
    if not tags:
        err_event = f'В файле {file_path} нет ни одного тега html!'
    return tags, err_event

def css_styles(file_path, cur_file_enc):
    """Вернуть список путей подгружаемых локальных css документов"""

    err_event = None  # возвращаемый текст ошибки
    styles = []  # возвращаемый список стилей
    if file_path is not None:
        with open (file_path, encoding=f'{cur_file_enc}') as f:
            for line in f:
                link_split = line.split()
                if link_split:
                    first_link_split = link_split[0]
                if (first_link_split == '<link') and (line.find('rel="stylesheet"') != -1):
                    for item in link_split:
                        if item.find('href="') != -1:
                            link = item
                            break
                    pos = link.find('href="') + 6  # номер первого символа стиля
                    if (link[pos:pos+4] != 'http'):  # если файл - локальный
                        if link.rfind('/') != -1:
                            styles.append(link[link.find('/')+1:-2].replace('/', '\\'))
                        else:
                            styles.append(link[pos:-2])
    if not styles:
        err_event = f'В файле {file_path} нет ни одного локального стиля!'
    return styles, err_event

def class_list(file_path, cur_file_enc):
    """Вернуть список классов"""

    css_classes = []
    with open (file_path, encoding=f'{cur_file_enc}') as f:
        for line in f:
            while (line.find('class="') != -1) and (line.find('<!--') == -1):
                cur_class = line[line.find('class="')+7:]
                line = cur_class[cur_class.find('"')+1:]
                cur_class = cur_class[:cur_class.find('"')]
                while (cur_class.find('{') != -1):  # обработка вложенных фигурных скобок
                    if (cur_class.rfind('{') > cur_class.find('}')):
                        cur_class = cur_class[:cur_class.find('{')] + cur_class[cur_class.find('}')+1:]
                    else:
                        cur_class = cur_class[:cur_class.rfind('{')] + cur_class[cur_class.find('}')+1:]
                cur_class = cur_class.split()
                for each_class in cur_class:
                    if each_class and each_class not in css_classes:
                        css_classes.append(each_class)
    return css_classes

def id_list(file_path, cur_file_enc):
    "Вернуть список идентификаторов"

    css_ids = []
    if file_path is not None:
        with open (file_path, encoding=f'{cur_file_enc}') as f:
            for line in f:
                while (line.find('id="') != -1) and (line.find('<!--') == -1):
                    cur_id = line[line.find('id="'):]
                    cur_id = cur_id[cur_id.find('"')+1:]
                    cur_id = cur_id[:cur_id.find('"')]
                    while (cur_id.find('{') != -1):  # обработка вложенных фигурных скобок
                        if (cur_id.rfind('{') > cur_id.find('}')):
                            cur_id = cur_id[:cur_id.find('{')] + cur_id[cur_id.find('}')+1:]
                        else:
                            cur_id = cur_id[:cur_id.rfind('{')] + cur_id[cur_id.find('}')+1:]
                    line = line[line.find('id="')+4:]
                    if cur_id and cur_id not in css_ids:
                        css_ids.append(cur_id)
    return css_ids

def css_work(file_path, cur_file_enc, all_used_tags, all_used_classes, all_used_ids):
    """Вернуть словарь {название класса/ID: его содержимое CSS} """

    global count_css_processed
    count_css_processed.append(file_path)
    used_css = {}  # словарь, хранящий весь значимый код css
    flag_sel_block = True  # true - смотрим селектор; false - смотрим блок
    flag_selector_found = False  # true - найден селектор; false - не найден
    flag_comments_found = False  # true - найден комментарий; false - не найден
    count_open = 0
    with open (file_path, encoding="utf8") as f:
        for line in f:
            if line.find("/*") != -1:
                flag_comments_found = True
            if flag_comments_found:
                if '*/' in line[-4:]:
                    flag_comments_found = False
            if not flag_comments_found:
                if flag_sel_block:
                    if (line.find("{") != -1) and (line.find("*/") == -1):
                        cur_selector = line[:line.find("{")].strip()
                        flag_selector_found = False

                        # < --- Глобальные селекторы
                        if cur_selector.find('@') != -1:  # если селектор - правило с '@'
                            count_open += 1
                            flag_selector_found = True
                            code_block = line[line.find("{"):]
                            if code_block.find('}') != -1:
                                used_css[cur_selector] = code_block
                                count_open = 0
                            else:
                                flag_sel_block = False
                        if not flag_selector_found and cur_selector == '*':  # если селектор - "*"
                            count_open += 1
                            flag_selector_found = True
                            code_block = line[line.find("{"):]
                            if code_block.find('}') != -1:
                                used_css[cur_selector] = code_block
                                count_open = 0
                            else:
                                flag_sel_block = False

                        # < --- Локальные селекторы
                        if not flag_selector_found:  # если селектор еще не найден
                            for cur_class in all_used_classes:  # проверяем селекторы классы
                                # регулярное выражение проверки класса
                                reg_exp = r'\.' + cur_class + r'($|:{1,2}.+$| *\,.+$| *\..+$|\[.+$| *\~.+$| *>.+$| *\+.+$)'
                                if re.search(reg_exp, cur_selector) is not None:
                                    count_open += 1
                                    flag_selector_found = True
                                    code_block = line[line.find("{"):]
                                    if code_block.find('}') != -1:
                                        used_css[cur_selector] = code_block
                                        count_open = 0
                                    else:
                                        flag_sel_block = False
                                if flag_selector_found:  # селектор найден, больше не просматриваем классы
                                    break
                        if not flag_selector_found:  # если классы не найдены - проверяем теги
                            cur_selector_tag = cur_selector.lower()
                            for cur_tag in all_used_tags:
                                # регулярное выражение проверки тега
                                reg_exp = r'([^\w\.]|^)' + cur_tag + r'($|:{1,2}.+$| *\,.+$| ?\..+$|\[.+$| *\~.+$| *>.+$| *\+.+$| +.+$)'
                                if re.search(reg_exp, cur_selector_tag) is not None:
                                    count_open += 1
                                    flag_selector_found = True
                                    code_block = line[line.find("{"):]
                                    if code_block.find('}') != -1:
                                        used_css[cur_selector] = code_block
                                        count_open = 0
                                    else:
                                        flag_sel_block = False
                                if flag_selector_found:  # селектор найден, больше не просматриваем теги
                                    break
                        if not flag_selector_found:  # классы и теги не найдены - проверяем идентификаторы
                            for cur_id in all_used_ids:
                                # регулярное выражение проверки идентификатора
                                reg_exp = r'\#' + cur_id + r'($|:{1,2}.+$| *\,.+$|\[.+$| *\~.+$| *>.+$| *\+.+$| +.+$)'
                                if re.search(reg_exp, cur_selector) is not None:
                                    count_open += 1
                                    flag_selector_found = True
                                    code_block = line[line.find("{"):]
                                    if code_block.find('}') != -1:
                                        used_css[cur_selector] = code_block
                                        count_open = 0
                                    else:
                                        flag_sel_block = False
                                if flag_selector_found:  # селектор найден, больше не просматриваем идентификаторы
                                    break
                else:
                    if line.find('{') != -1:
                        count_open += 1 
                    if line.find('}') == -1:
                        code_block += line
                    elif line.find('}') != -1 and count_open>1:
                        count_open -= 1
                        code_block += line
                    elif line.find('}') != -1 and count_open==1:
                        count_open = 0
                        code_block += line
                        used_css[cur_selector] = code_block
                        flag_sel_block = True
    return used_css

def new_css(file_path, cur_file_enc, css_dictionary):
    """Создает новые оптимизированные css файлы"""

    file_path = file_path[:file_path.rfind('\\')+1] + '_' + file_path[file_path.rfind('\\')+1:]
    css_file = open (file_path, 'w', encoding=f'{cur_file_enc}')
    for cur_selector in css_dictionary:
        cur_value = css_dictionary[cur_selector]
        css_file.write(cur_selector + ' ' + cur_value)
    css_file.close()
    return None

def new_html(file_path, cur_file_enc, css_docs):
    """Создает новый html файл, меняет ссылки на локальные стили в нем"""

    new_file_path = file_path[:file_path.rfind('\\')+1] + '_' + file_path[file_path.rfind('\\')+1:]
    new_html_file = open (new_file_path, 'w', encoding=f'{cur_file_enc}')
    with open(file_path, encoding=f'{cur_file_enc}') as f:
        for line in f:
            if line.find("href") == -1:
                new_html_file.write(line)
            else:
                style_found = False
                href = line[line.find("href"):]  # обрезаем содержимое href
                href = href[href.find('"')+1:]
                href = href[:href.find('"')]
                for css_doc in css_docs:
                    css_doc = css_doc.replace('\\', '/')
                    if href.find(css_doc) != -1:
                        style_found = True
                        if href.find('/') == -1:
                            new_line = line[:line.find(css_doc)] + '_' + line[line.find(css_doc):]
                            new_html_file.write(new_line)
                        else:
                            href = href[:href.rfind('/')+1] + '_' + href[href.rfind('/')+1:]
                            line2 = line[line.find('href="')+6:]
                            line2 = line2[line2.find('"'):]
                            new_line = line[:line.find('href="')+6] + href + line2
                            new_html_file.write(new_line)
                        break
                if not style_found:
                    new_html_file.write(line)
    return None

def stats(count_css_processed):
    """Вернуть статистику об обработанных css файлах"""

    print('Размер css файлов:')
    base = []
    opt = []
    for css_file in count_css_processed:
        size = os.path.getsize(css_file)  # размер css файла до оптимизации
        css_file1 = css_file[css_file.rfind('\\')+1:]
        base.append(size/1024)
        print(f' {css_file1}: {round(size/1024, 2)} kbytes')
        css_file = css_file[:css_file.rfind('\\')+1] + '_' + css_file[css_file.rfind('\\')+1:]
        size = os.path.getsize(css_file)  # размер css файла после оптимизации
        css_file1 = css_file[css_file.rfind('\\')+1:]
        opt.append(size/1024)
        print (f'{css_file1}: {round(size/1024, 2)} kbytes')
    percent = round((1-sum(opt)/sum(base))*100, 2)
    print(f'Оптимизация составила {percent}%')

    return None

if __name__ == "__main__":

    _tmp = f'''Проверьте правильность заполнения run.bat!!!
Файл должен быть заполнен по шаблону ("<", ">" ставить не надо, "_" - означает пробел):
{"-":-<130}
<путь до интерпретатора python>_<-O>_<htmltags.py>_<путь или директория до файла(-ов) HTML>_<путь или директория до файла(-ов) CSS>
{"-":-<130}
Например: C:\\Users\\Python\\Python38-32\\python.exe -O htmltags.py C:\\Users\\Documents\\HTML C:\\Users\\Documents\\HTML\\css'''
    try: 
        (sys.argv[1] and sys.argv[2])
    except IndexError:
        html_path = r'C:\Users\xiaomi\Documents\GitHub\practice1\HTML'
        css_path = r'C:\Users\xiaomi\Documents\GitHub\practice1\HTML\css'
    else:
        html_path = sys.argv[1]  # папка или файл с html файлами
        css_path = sys.argv[2]  # папка с css файлами """
    all_html_docs, all_css_docs = html_css_existence(html_path, css_path)
    if all_html_docs and all_css_docs:  # если передали хотя бы 1 html файл и хотя бы 1 css файл
        count_css_processed = []
        all_tags = []
        all_styles = []
        all_classes = []
        all_ids = []
        for each_html_doc in all_html_docs:
            all_used_tags = []
            styles = []
            all_used_classes = []
            all_used_ids = []
            cur_file_enc = encoding(each_html_doc)  # определяем кодировку файла
            # --- Шаг 1
            # Получение списка тегов из всех html документов
            all_used_tags, err_event = html_tags(each_html_doc, cur_file_enc)
            for each_tag in all_used_tags:
                if each_tag and each_tag not in all_tags:
                    all_tags.append(each_tag)
            # --- Шаг 2
            # Получение списка всех подгружаемых каскадных таблиц
            styles, err_event = css_styles(each_html_doc, cur_file_enc)
            for each_style in styles:
                if each_style and each_style not in all_styles:
                    all_styles.append(each_style)
            # --- Шаг 3
            # Получение списка классов и идентификаторов
            all_used_classes = class_list(each_html_doc, cur_file_enc)  # список классов
            for each_class in all_used_classes:
                if each_class and each_class not in all_classes:
                    all_classes.append(each_class)
            all_used_ids = id_list(each_html_doc, cur_file_enc)  # список идентификаторов
            for each_id in all_used_ids:
                if each_id and each_id not in all_ids:
                    all_ids.append(each_id)
        # получен список тегов
        print ("HTML tags:")
        [print(x.upper()) for x in all_tags]
        # получен список локальных стилей
        print ("\nLocal CSS styles:")
        [print(x) for x in all_styles]
        # получен список идентификаторов
        print ("\nID list:")
        [print(x) for x in all_ids]
        # получен список используемых классов
        print ("\nClass list:")
        [print(x) for x in all_classes]
        # --- Шаг 4
        # Обработка CSS документов
        css_docs = []
        for css_doc in all_styles:
            flag_file_found = False
            for real_css_doc in all_css_docs:
                if css_doc in real_css_doc:
                    flag_file_found = True
                    cur_file_enc = encoding(real_css_doc)
                    css_docs.append(css_work(real_css_doc, cur_file_enc, all_tags, all_classes, all_ids))
                    break
            if not flag_file_found:
                print (f'Файл {css_doc} не был обработан, т.к. не находится в указанной директории')
        # --- Шаг 5
        # Создание минимизированных файлов
        dict_num = 0
        for css_doc in all_styles:
            for real_css_doc in all_css_docs:
                if css_doc in real_css_doc:
                    cur_file_enc = encoding(real_css_doc)
                    new_css(real_css_doc, cur_file_enc, css_docs[dict_num])  # создаются минимизированные файлы css
                    dict_num += 1
                    break
        for each_html_doc in all_html_docs:
            cur_file_enc = encoding(each_html_doc)
            new_html(each_html_doc, cur_file_enc, all_styles)  # создается новый html файл
        # Вывод названия обработанных файлов
        print(f'Обработано {len(count_css_processed)} CSS файла:')
        [print(x) for x in count_css_processed]
        stats(count_css_processed)
    else:
        print(_tmp)