# Лебедев Евгений Получение оптимизационного файла (минимизация структуры подгружаемых каскадных таблиц в HTML)
import os

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
                tag1 = line.split()
                if tag1:
                    tag2 = tag1[0].split('>')
                    tag = tag2[0]
                # проверка на открывающий и уникальный тег
                if (tag[0] == '<') and (tag[1].isalpha()) and (tag[1:] not in tags):
                    tags.append(tag[1:])
    if not tags:
        err_event = "Нет ни одного тега html!"
    return tags, err_event

def class_list(file_path, tags):
    """Вернуть для каждого тега список классов"""

    css_classes = {}
    if err_event is None:
        # теги до body - не существенные
        for i,tag in enumerate(tags):
            if tag == 'body':
                pos_body = i
                break
        s_tags = tags[pos_body+1:]  # существенные теги
        for tag in s_tags:
            class_list = []
            with open (file_path) as f:
                for line in f:
                    if f'<{tag}' in line:
                        pos1 = line.find(f'{tag}')
                        line2 = line[pos1:]
                        pos2 = line2.find('>')
                        cur_tag = line2[:pos2]
                        if 'class="' in cur_tag:
                            cur_class2 = cur_tag[cur_tag.find('class="')+7:]
                            cur_class = cur_class2[:cur_class2.find('"')]
                            if cur_class and cur_class not in class_list:
                                class_list.append(cur_class)
            css_classes[f'{tag}'] = class_list
    return css_classes


def css_styles():
    """Вернуть список путей подгружаемых локальных css документов"""

    err_event = None  # возвращаемый текст ошибки
    styles = []  # возвращаемый список стилей
    if file_path is not None:
        with open (file_path) as f:
            for line in f:
                link_split = line.split()
                if link_split:
                    first_link_split = link_split[0]
                if (first_link_split == '<link') and (line.find('rel="stylesheet"')!=-1):
                    for item in link_split:
                        if item.find('href="')!=-1:
                            link = item
                            break
                    pos = link.find('href="') + 6  # номер первого символа стиля
                    if (link[pos:pos+5] != 'https'):  # если файл - локальный
                        styles.append(link[link.rfind('/')+1:-2])
    if not styles:
        err_event = "Нет ни одного локального стиля!"
    return styles, err_event


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
            styles, err_event = css_styles()
            if err_event is None:
                # получен список локальных стилей
                print ("Local CSS styles:")
                [print(x) for x in styles]
                # --- Шаг 3
                classes = class_list(file_path, tags)
                # список классов для каждого тега
                print (classes)
            else:
            # ошибка формирования списка локальных стилей
                print(err_event)
        else:
        # ошибка формирования списка html тегов
            print(err_event)
    else:
        # ошибка существования файла
        print(err_event)