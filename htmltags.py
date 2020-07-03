# Лебедев Евгений Получение оптимизационного файла (минимизация структуры подгружаемых каскадных таблиц в HTML)
import os, re

class Htmlobject:
    """Класс, описывающий объект HTML"""

    def __init__ (self, tag_name, class_names):  # инициализация
        self.tag_name = tag_name
        self.class_names = class_names

    def htmlobject_print(self):
        print(f'\nТег: {self.tag_name}\nИспользуемые классы CSS: {self.class_names}')  # вывод информации об объекте
        

def file_existence(_targetFile):
    """Вернуть путь к файлу, если файл существует"""

    err_event = None  # возвращаемый текст ошибки
    folderslist = ["practice1", "Git"]  # список корневых папок
    cur_dir = os.getcwd()
    file_path = None  # путь к обрабатываему файлу
    for item in folderslist:
        work_dir = f'{cur_dir[:cur_dir.rfind(item)+len(item)]}\\HTML'
        _tmp = f'{work_dir}\\{_targetFile}'
        # проверка существования файла
        if os.path.isfile(_tmp):
            file_path = _tmp
            break
    if file_path is None:
        err_event = "Файл отсутствует!"
    return file_path, err_event

def html_tags(file_path):
    """Вернуть список тегов"""

    err_event = None  # возвращаемый текст ошибки
    tags = []  # возвращаемый список переменных
    if file_path is not None:
        with open (file_path) as f:
            for line in f:
                while (line.find('<') != -1):
                    line = line[line.find('<'):]
                    split_lines = line.split()
                    first_tag = split_lines[0].split('>')
                    tag = first_tag[0]
                    # проверка на открывающий и уникальный тег
                    if (tag[0] == '<') and (tag[1].isalpha()) and (tag[1:] not in tags):
                        tags.append(tag[1:])
                    line = line[line.find(f'{tag}')+len(tag)+1:]
    if not tags:
        err_event = "Нет ни одного тега html!"
    return tags, err_event

def css_styles(file_path):
    """Вернуть список путей подгружаемых локальных css документов"""

    err_event = None  # возвращаемый текст ошибки
    styles = []  # возвращаемый список стилей
    if file_path is not None:
        with open (file_path) as f:
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
                    if (link[pos:pos+5] != 'https'):  # если файл - локальный
                        styles.append(link[link.rfind('/')+1:-2])
    if not styles:
        err_event = "Нет ни одного локального стиля!"
    return styles, err_event

def class_list(file_path, tags):
    """Вернуть для каждого тега список классов"""

    css_classes = {}
    if err_event is None:
        for tag in tags:
            class_list = []
            with open (file_path) as f:
                for line in f:
                    if f'<{tag}' in line:
                        pos1 = line.find(f'{tag}')
                        line = line[pos1:]
                        pos2 = line.find('>')
                        cur_tag = line[:pos2]
                        if 'class="' in cur_tag:
                            cur_class = cur_tag[cur_tag.find('class="')+7:]
                            cur_class = cur_class[:cur_class.find('"')]
                            cur_classes = cur_class.split()
                            for each_cur_class in cur_classes:
                                if each_cur_class and each_cur_class not in class_list:
                                    class_list.append(each_cur_class)
            css_classes[f'{tag}'] = class_list
    return css_classes

def all_used_css(dict_tag_class):
    "Из словаря вернуть список тегов и список уникальных классов"

    all_used_tags = list(dict_tag_class.keys())  # список всех используемых тегов в html
    all_used_classes = []  # список всех используемых классов в html
    for elem in dict_tag_class: 
        value = dict_tag_class[elem]
        for cur_value in value:
            if cur_value and cur_value not in all_used_classes:
                all_used_classes.append(cur_value)
    return all_used_tags, all_used_classes

def css_work(file_path, all_used_tags, all_used_classes):
    """Вернуть словарь {название класса/ID: его содержимое CSS} """

    print(f'\nФайл CSS {file_path}')
    used_css = {}  # словарь, хранящий весь значимый код css
    flag_sel_block = True  # true - смотрим селектор; false - смотрим блок
    flag_selector_found = False  # true - найден селектор; false - не найден
    with open (file_path) as f:
        for line in f:
            if flag_sel_block:
                if (line.find("{")) != -1:
                    cur_selector = line[:line.find("{")].strip()
                    for cur_class in all_used_classes:  # проверяем селекторы классы
                        reg_exp = '.' + cur_class + r'($|:{1,2}.+$)'
                        if re.match(reg_exp, cur_selector) is not None:
                            flag_selector_found = True
                            code_block = line[line.find("{"):]
                            if code_block.find('}') != -1:
                                used_css[cur_selector] = code_block
                            else:
                                flag_sel_block = False
                        if flag_selector_found:  # селектор найден, больше не просматриваем классы
                            flag_selector_found = False
                            break
            else: 
                if line.find('}') == -1:
                    code_block += line
                else:
                    code_block += line
                    used_css[cur_selector] = code_block
                    flag_sel_block = True
    for selector in used_css:
        block = used_css[selector]
        print(f'{selector} {block}')
    #print (f'Used_css: {used_css}')

if __name__ == "__main__":

    _targetFile = "index.html"
    file_path, err_event = file_existence(_targetFile)
    # --- Шаг 1
    if file_path is not None:
        tags, err_event = html_tags(file_path)
        if err_event is None:
            # получен список тегов
            print ("HTML tags:")
            [print(x.upper()) for x in tags]
            # --- Шаг 2
            styles, err_event = css_styles(file_path)
            if err_event is None:
                # получен список локальных стилей
                print ("Local CSS styles:")
                [print(x) for x in styles]
                # --- Шаг 3
                classes = class_list(file_path, tags)
                # Формирование списка объектов класса
                myobjects = []
                for elem in classes:  # для каждого объекта словаря
                    value = classes[elem]
                    myobjects.append(Htmlobject(elem, value))
                # Вывод информации об объектах
                for obj in myobjects:
                    obj.htmlobject_print()
                # --- Шаг 4
                # Обработка CSS документов
                css_docs = []
                all_used_tags, all_used_classes = all_used_css(classes)
                for css_doc in styles:
                    file_path, err_event = file_existence(css_doc)
                    if err_event is None:
                        css_docs.append(css_work(file_path, all_used_tags, all_used_classes)) 
                    else:
                    # ошибка существования css файла
                        print(err_event)
            else:
            # ошибка формирования списка локальных стилей
                print(err_event)
        else:
        # ошибка формирования списка html тегов
            print(err_event)
    else:
        # ошибка существования файла
        print(err_event)
