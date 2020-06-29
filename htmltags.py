# Лебедев Евгений Получение списка html тегов документа
import os

_sl = ["practice1", "Git"]     #Список корневых папок
t = os.getcwd()
_rF = None
for item in _sl:
    _wd = f'{t[:t.rfind(item)+len(item)]}\\HTML'     
    if os.path.isfile(f'{_wd}\\index.html'):   #Проверка существования файла
        _rF = _wd
        break

if _rF is not None:
    tags = []
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
        print ("Список тегов:")
        for i in tags:
            print (i, end=' ')
else:
    print ("Файл отсутствует!")