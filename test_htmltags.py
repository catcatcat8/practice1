# Лебедев Евгений Тестирование скрипта на двух существующих файлах
import re, htmltags

targetFiles = ["index.html", "errresult.html"]

def test_file_existence():
    """Тест проверки существования файла"""

    for cur_file in targetFiles:
        file_path, err_event = htmltags.file_existence(cur_file)
        assert file_path, f'{err_event}'

def test_html_tags():
    """Тест проверки списка возвращаемых тегов"""

    list_tags_indexhtml = ['html', 'head', 'title', 'meta', 'link', 'script', 'body', 
    'div', 'form', 'span', 'input', 'p', 'ul', 'li']
    list_tags_errresulthtml = ['p', 'span', 'div', 'ul', 'li']

    file_path, err_event = htmltags.file_existence('index.html')
    tags, err_event = htmltags.html_tags(file_path, 'utf-8')
    assert tags==list_tags_indexhtml, f'{err_event}'  # список тегов index.html

    file_path, err_event = htmltags.file_existence('errresult.html')
    tags, err_event = htmltags.html_tags(file_path, 'utf-8')
    assert tags == list_tags_errresulthtml, f'{err_event}'  # список тегов errresult.html

def test_css_styles():
    """Тест проверки возвращаемых локальных css документов"""

    list_styles_indexhtml = ['util.css', 'main.css']  # список локальных стилей index.html

    file_path, err_event = htmltags.file_existence('index.html')
    styles, err_event = htmltags.css_styles(file_path, 'utf-8')
    assert styles == list_styles_indexhtml, f'{err_event}'

    file_path, err_event = htmltags.file_existence('errresult.html')
    styles, err_event = htmltags.css_styles(file_path, 'utf-8')
    assert not styles, f'{err_event}'  # ни одного локального стиля в errresult.html

def test_class_list():
    """Тест проверки возвращаемых классов css"""

    list_classes_indexhtml = ['limiter', 'container-login100', 'wrap-login100', 'p-t-10', 'p-b-90', 
    'login100-form', 'validate-form', 'flex-sb', 'flex-w', 'm-b-20', 'login100-form-title', 'm-b-10', 'wrap-input100', 
    'validate-input', 'm-b-16', 'input100', 'container-login100-form-btn', 'm-t-17', 'login100-form-btn', 'm-l-10',
    'pc', 'fs-12', 'ab-b-l']  # список классов index.html
    list_classes_errresulthtml = ['input80', 'm-b-20', 'fs-20', 'wrap-login90', 'p-b-10', 'm-t-20', 
    'm-t-40', 'm-b-10', 'm-l-10', 'pc', 'fs-12', 'wrap-login100', 'p-t-10', 'p-b-90', 'ab-b-l']  # список классов errresult.html

    file_path, err_event = htmltags.file_existence('index.html')
    classes = htmltags.class_list(file_path, 'utf-8')
    assert classes == list_classes_indexhtml, f'{err_event}'

    file_path, err_event = htmltags.file_existence('errresult.html')
    classes = htmltags.class_list(file_path, 'utf-8')
    assert classes == list_classes_errresulthtml,  f'{err_event}'

def test_id_list():
    """Тест проверки возвращаемых идентификаторов css"""

    list_ids_examhtml = ['section_start', 'accordion', 'ques', 'collapse', 'sendresult']  # список идентификаторов exam.html
    file_path, err_event = htmltags.file_existence('exam.html')
    id_list = htmltags.id_list(file_path, 'utf-8')
    assert id_list == list_ids_examhtml,  f'{err_event}'

def test_selectors():
    """Тест проверки отбора селекторов"""

    list_selectors = ['h1', '@font-face', '*', 'h1, h2, h3, h4, h5, h6', 'div',  'a:hover', '.class1', '.class666', 
    '.class2.class1', '#id1', 'li a', '.class2::pseudo2', '.x + .y', '.x > .y',
    ':lang(en) .custom-file-input ~ .custom-file-label::after',
    '.navbar-nav.mainUser > li.nav-item .nav-link:hover',
    'main .WndRegist .WndPanel .WellItem[data-isactive="1"]']  # список селекторов
    tag_class_id_list = ['h1', 'h2', 'h6', 'a', 'class1', 'class2', 'id1', 'x', 'y', 'body', 'html', 
    'custom-file-label', 'nav-link', 'WellItem']  # список используемых тегов, классов, id
    expected_result = [True, True, True, True, False, True, True, False, 
    True, True, True, True, True, True, True, True, True,]  # ожидаемый результат
    received_result = []

    # фрагмент кода из метода css_work
    for cur_selector in list_selectors:
        flag_selector_found = False
        if cur_selector.find('@') != -1:  # если селектор - правило с '@'
            flag_selector_found = True
            received_result.append(True)
        if not flag_selector_found and cur_selector == '*':  # если селектор - "*"
            flag_selector_found = True
            received_result.append(True)
        if not flag_selector_found:  # если селектор еще не найден
            for cur_class in tag_class_id_list:  # проверяем селекторы классы
                # регулярное выражение проверки класса
                reg_exp = r'\.' + cur_class + r'($|:{1,2}.+$| *\,.+$| *\..+$|\[.+$| *\~.+$| *>.+$| *\+.+$)'
                if re.search(reg_exp, cur_selector) is not None:
                    flag_selector_found = True
                    received_result.append(True)
                    break
        if not flag_selector_found:  # если классы не найдены - проверяем теги
            for cur_tag in tag_class_id_list:
                # регулярное выражение проверки тега
                reg_exp = r'([^\w\.]|^)' + cur_tag + r'($|:{1,2}.+$| *\,.+$| ?\..+$|\[.+$| *\~.+$| *>.+$| *\+.+$| +.+$)'
                if re.search(reg_exp, cur_selector) is not None:
                    flag_selector_found = True
                    received_result.append(True)
                    break
        if not flag_selector_found:  # классы и теги не найдены - проверяем идентификаторы
            for cur_id in tag_class_id_list:
                # регулярное выражение проверки идентификатора
                reg_exp = r'\#' + cur_id + r'($|:{1,2}.+$| *\,.+$|\[.+$| *\~.+$| *>.+$| *\+.+$| +.+$)'
                if re.search(reg_exp, cur_selector) is not None:
                    flag_selector_found = True
                    received_result.append(True)
                    break
        if not flag_selector_found:
            received_result.append(False)
    
    assert expected_result == received_result