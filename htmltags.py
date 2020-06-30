# Лебедев Евгений Получение списка html тегов документа
import os

def read_file():
    """Вернуть список тегов"""

    tags = []  # возвращаемый список переменных
    err_event = None  # возвращаемый текст ошибки
    _sl = ["practice1", "Git"]  # Список корневых папок
    t = os.getcwd()
    _rF = None  # путь к обрабатываему файлу
    for item in _sl:
        _wd = f'{t[:t.rfind(item)+len(item)]}\\HTML'
        # Проверка существования файла
        if os.path.isfile(f'{_wd}\\index.html'):
            _rF = _wd
            break
    if _rF is not None:
        
        with open (f'{_rF}\\index.html') as f:
            for line1 in range(1):
                next(f)
            for line in f:
                tag1 = line.split()
                if tag1:
                    tag2 = tag1[0].split('>')
                    tag = tag2[0]
                if (tag[0] == '<') and (tag[1] != '/') and (tag[1:] not in tags):
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

