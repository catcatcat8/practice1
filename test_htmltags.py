# Лебедев Евгений: Тестирование
import re
import logic
import pytest

html_path1 = 'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\index.html'
html_path2 = 'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\errresult.html'
css_path = 'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\css'

def test_html_css_existence():
    """Тест проверки списка возвращаемых по пути"""

    list_css_docs = [
    'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\css\\font-awesome.min.css',
    'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\css\\main.css',
    'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\css\\util.css'
    ]
    all_html_docs, all_css_docs = logic.html_css_existence(html_path1, css_path)
    assert all_html_docs==[html_path1]
    assert all_css_docs==list_css_docs
    all_html_docs, all_css_docs = logic.html_css_existence(html_path2, css_path)
    assert all_html_docs==[html_path2]
    assert all_css_docs==list_css_docs

def test_html_tags():
    """Тест проверки списка возвращаемых тегов"""

    list_tags_indexhtml = ['html', 'head', 'title', 'meta', 'link', 'script', 'body', 
    'div', 'form', 'span', 'input', 'p', 'ul', 'li']
    list_tags_errresulthtml = ['p', 'span', 'div', 'ul', 'li']

    tags, err_event = logic.html_tags(html_path1, 'utf-8')
    assert tags==list_tags_indexhtml, 'ошибка списка тегов "index.html"'  # список тегов index.html

    tags, err_event = logic.html_tags(html_path2, 'utf-8')
    assert tags == list_tags_errresulthtml, 'ошибка списка тегов "errresult.html"'  # список тегов errresult.html

def test_css_styles():
    """Тест проверки возвращаемых локальных css документов"""

    list_styles_indexhtml = ['css\\util.css', 'css\\main.css']  # список локальных стилей index.html

    styles, err_event = logic.css_styles(html_path1, 'utf-8')
    assert styles == list_styles_indexhtml, 'ошибка списка css документов "index.html"'

    styles, err_event = logic.css_styles(html_path2, 'utf-8')
    assert not styles, 'ошибка списка css документов "errresult.html"'  # ни одного локального стиля в errresult.html

def test_class_list():
    """Тест проверки возвращаемых классов css"""

    list_classes_indexhtml = ['limiter', 'container-login100', 'wrap-login100', 'p-t-10', 'p-b-90', 
    'login100-form', 'validate-form', 'flex-sb', 'flex-w', 'm-b-20', 'login100-form-title', 'm-b-10', 'wrap-input100', 
    'validate-input', 'm-b-16', 'input100', 'container-login100-form-btn', 'm-t-17', 'login100-form-btn', 'm-l-10',
    'pc', 'fs-12', 'ab-b-l']  # список классов index.html
    list_classes_errresulthtml = ['input80', 'm-b-20', 'fs-20', 'wrap-login90', 'p-b-10', 'm-t-20', 
    'm-t-40', 'm-b-10', 'm-l-10', 'pc', 'fs-12', 'wrap-login100', 'p-t-10', 'p-b-90', 'ab-b-l']  # список классов errresult.html

    classes = logic.class_list(html_path1, 'utf-8')
    assert classes == list_classes_indexhtml, 'ошибка списка классов "index.html"'

    classes = logic.class_list(html_path2, 'utf-8')
    assert classes == list_classes_errresulthtml, 'ошибка списка классов "errresult.html"'

def test_id_list():
    """Тест проверки возвращаемых идентификаторов css"""

    list_ids_examhtml = ['section_start', 'accordion', r'ques{{item[6]}}', r'collapse{{item[6]}}',
    'sendresult']  # список идентификаторов exam.html
    exam_html_path = 'C:\\Users\\xiaomi\\Documents\\GitHub\\practice1\\HTML\\exam.html'
    id_list = logic.id_list(exam_html_path, 'utf-8')
    assert id_list == list_ids_examhtml,  'ошибка списка id "exam.html"'

def test_selectors():
    """Тест проверки отбора селекторов"""

    list_selectors = ['h1', 'H1', '@font-face', '*', 'h1, h2, h3, h4, h5, h6', 'div',  'a:hover', '.class1', '.class666', 
    '.class2.class1', '#id1', 'li a', '.class2::pseudo2', '.x + .y', '.x > .y',
    ':lang(en) .custom-file-input ~ .custom-file-label::after',
    '.navbar-nav.mainUser > li.nav-item .nav-link:hover',
    'main .WndRegist .WndPanel .WellItem[data-isactive="1"]']  # список селекторов
    tag_class_id_list = ['h1', 'h2', 'h6', 'a', 'class1', 'class2', 'id1', 'x', 'y', 'body', 'html', 
    'custom-file-label', 'nav-link', 'WellItem']  # список используемых тегов, классов, id
    expected_result = [True, True, True, True, True, False, True, True, False, 
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
            cur_selector_tag = cur_selector.lower()
            for cur_tag in tag_class_id_list:
                # регулярное выражение проверки тега
                reg_exp = r'([^\w\.]|^)' + cur_tag + r'($|:{1,2}.+$| *\,.+$| ?\..+$|\[.+$| *\~.+$| *>.+$| *\+.+$| +.+$)'
                if re.search(reg_exp, cur_selector_tag) is not None:
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
    
    assert expected_result == received_result, 'ошибка разбора селекторов'

if __name__ == "__main__":
    pytest.main()
