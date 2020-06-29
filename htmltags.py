import os
file_path = '/Users/xiaomi/Documents/GitHub/practice1/HTML/index.html'
t = os.getcwd()
_wd = f'{t[:t.rfind("Git")+3]}\\HTML'

if os.path.isfile(f'{_wd}\\index.html'):
    tags = []
    with open (file_path) as f:
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