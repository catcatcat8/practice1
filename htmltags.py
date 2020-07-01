# Лебедев Евгений Получение оптимизационного файла (минимизация структуры подгружаемых каскадных таблиц в HTML)
import os

def file_existence():
    """Вернуть путь к файлу, если файл существует"""

    err_event = None  # возвращаемый текст ошибки
    folderslist = ["practice1", "Git"]  # список корневых папок
    cur_dir = os.getcwd()
    file_path = None  # путь к обрабатываему файлу
    for item in folderslist:
        work_dir = f'{cur_dir[:cur_dir.rfind(item)+len(item)]}\\HTML'
        # проверка существования файла
        if os.path.isfile(f'{work_dir}\\index.html'):
            file_path = work_dir
            break
    if file_path is None:
        err_event = "Файл отсутствует!"
    return file_path, err_event

def html_tags():
    """Вернуть список тегов"""

    tags = []  # возвращаемый список переменных
    file_path, err_event = file_existence()
    if file_path is not None:
        with open (f'{file_path}\\index.html') as f:
            for line in f:
                tag1 = line.split()
                if tag1:
                    tag2 = tag1[0].split('>')
                    tag = tag2[0]
                # проверка на открывающий и уникальный тег
                if (tag[0] == '<') and (tag[1].isalpha()) and (tag[1:] not in tags):
                    tags.append(tag[1:])
    return tags, err_event

def class_list(tags):
    """Вернуть для каждого тега список классов"""

    file_path, err_event = file_existence()
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
            with open (f'{file_path}\\index.html') as f:
                for line in f:
                    if f'{tag} class' in line:
                        pos = line.find('class="')
                        cur_class1 = line[pos+7:]
                        cur_class = cur_class1[:cur_class1.find('"')]
                        if cur_class not in class_list:
                            class_list.append(cur_class)
            css_classes[f'{tag}'] = class_list
    return css_classes


def css_styles():
    """Вернуть список путей подгружаемых локальных css документов"""

    styles = []  # возвращаемый список стилей
    file_path, err_event = file_existence()
    if file_path is not None:
        with open (f'{file_path}\\index.html') as f:
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
    return styles, err_event


if __name__ == "__main__":

    # --- Шаг 1
    tags, err_event = html_tags()
    if err_event is None:
        # получен список тегов
        print ("HTML tags:")
        [print(x.upper()) for x in tags]
    else:
       # ошибка формирования списка
        print(err_event)

    # --- Шаг 2
    styles, err_event = css_styles()
    if err_event is None:
        # получен список локальных стилей
        print ("Local CSS styles:")
        [print(x) for x in styles]
    else:
       # ошибка формирования списка
        print(err_event)

    # --- Шаг 3
    classes = class_list(tags)
    print (classes)
