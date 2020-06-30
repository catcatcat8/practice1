# Лебедев Евгений Получение оптимизационного файла (минимизация структуры подгружаемых каскадных таблиц в HTML)
import os

def read_file():
    """Вернуть список тегов"""

    tags = []  # возвращаемый список переменных
    err_event = None  # возвращаемый текст ошибки
    folderslist = ["practice1", "Git"]  # Список корневых папок
    cur_dir = os.getcwd()
    file_path = None  # путь к обрабатываему файлу
    for item in folderslist:
        work_dir = f'{cur_dir[:cur_dir.rfind(item)+len(item)]}\\HTML'
        # Проверка существования файла
        if os.path.isfile(f'{work_dir}\\index.html'):
            file_path = work_dir
            break
    if file_path is not None:
        
        with open (f'{file_path}\\index.html') as f:
            for line in f:
                tag1 = line.split()
                if tag1:
                    tag2 = tag1[0].split('>')
                    tag = tag2[0]
                if (tag[0] == '<') and (tag[1].isalpha()) and (tag[1:] not in tags):
                    tags.append(tag[1:])
    else:
        err_event = "Файл отсутствует!"
    return tags, err_event


if __name__ == "__main__":
    tags, err_event = read_file()
    if err_event is None:
        # получен список тегов
        [print(x.upper()) for x in tags]
    else:
       # ошибка формирования списка
        print(err_event)

