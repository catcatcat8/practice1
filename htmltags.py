# e3rewrertfregtr
import os

_sl = ["practice1", "Git"]
t = os.getcwd()
_rF =None
for item in _sl:
    _wd = f'{t[:t.rfind(item)+len(item)]}\\HTML'
    if os.path.isfile(f'{_wd}\\index.html'):
        _fr = _wd1
        break

if _rF is not None:
    tags = []
    with open (_rF) as f:
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