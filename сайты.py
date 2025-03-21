from xml.dom.minidom import Document

# Глобальный объект документа
документ = Document()
html = None
body = None

def создать_элемент(имя_тега, **атрибуты):
    """
    Создает HTML-элемент с указанным тегом и атрибутами.
    """
    элемент = документ.createElement(имя_тега)
    for атрибут, значение in атрибуты.items():
        элемент.setAttribute(атрибут, значение)
    return элемент

def создать_текстовый_узел(text):
    """
    Создает текстовый узел с указанным текстом.
    """
    return документ.createTextNode(str(text))

def добавить_элемент(родитель_элемента, потомок_элемента):
    """
    Добавляет дочерний элемент к родительскому.
    """
    if потомок_элемента:  # Защита от None
        родитель_элемента.appendChild(потомок_элемента)

def создать_html():
    """
    Инициализирует базовую структуру HTML.
    """
    global документ, html, body
    документ = Document()
    html = создать_элемент('html')
    документ.appendChild(html)
    
    # Создаем head с мета-тегами
    head = создать_элемент('head')
    добавить_элемент(html, head)
    
    meta_charset = создать_элемент('meta', charset="UTF-8")
    meta_viewport = создать_элемент('meta', 
        name="viewport", 
        content="width=device-width, initial-scale=1.0"
    )
    добавить_элемент(head, meta_charset)
    добавить_элемент(head, meta_viewport)
    
    # Создаем body
    body = создать_элемент('body')
    добавить_элемент(html, body)

def добавить_заголовок_страницы(заголовок):
    """
    Добавляет заголовок страницы в <title>.
    """
    head = html.getElementsByTagName('head')[0]
    title = создать_элемент('title')
    title.appendChild(создать_текстовый_узел(заголовок))
    добавить_элемент(head, title)

def добавить_заголовок(уровень, text, **атрибуты):
    """
    Создает заголовок от h1 до h6.
    """
    тег = f'h{уровень}'
    заголовок = создать_элемент(тег, **атрибуты)
    заголовок.appendChild(создать_текстовый_узел(text))
    return заголовок

def добавить_абзац(text, **атрибуты):
    """
    Создает абзац.
    """
    p = создать_элемент('p', **атрибуты)
    p.appendChild(создать_текстовый_узел(text))
    return p

def добавить_ссылку(text, url, **атрибуты):
    """
    Создает ссылку.
    """
    ссылка = создать_элемент('a', href=url, **атрибуты)
    ссылка.appendChild(создать_текстовый_узел(text))
    return ссылка

def добавить_список(элементы, упорядоченный=False, **атрибуты):
    """
    Создает список (упорядоченный или неупорядоченный).
    """
    тег = 'ol' if упорядоченный else 'ul'
    список = создать_элемент(тег, **атрибуты)
    for элемент in элементы:
        пункт = создать_элемент('li')
        текст_узла = создать_текстовый_узел(элемент)
        добавить_элемент(пункт, текст_узла)
        добавить_элемент(список, пункт)
    return список

def добавить_изображение(src, alt="", **атрибуты):
    """
    Создает изображение.
    """
    return создать_элемент('img', src=src, alt=alt, **атрибуты)

def добавить_iframe(src, **атрибуты):
    """
    Создает iframe для встраивания контента.
    """
    return создать_элемент('iframe', src=src, **атрибуты)

def добавить_таблицу(строки, **атрибуты):
    """
    Создает таблицу.
    """
    таблица = создать_элемент('table', **атрибуты)
    for строка in строки:
        tr = создать_элемент('tr')
        for ячейка in строка:
            td = создать_элемент('td')
            текст_узла = создать_текстовый_узел(ячейка)
            добавить_элемент(td, текст_узла)
            добавить_элемент(tr, td)
        добавить_элемент(таблица, tr)
    return таблица

def добавить_форму(метод="post", действие="", **атрибуты):
    """
    Создает форму.
    """
    return создать_элемент('form', method=метод, action=действие, **атрибуты)

def добавить_поле_ввода(тип_обьекта, имя, **атрибуты):
    """
    Создает поле ввода.
    """
    return создать_элемент('input', type=тип_обьекта, name=имя, **атрибуты)

def добавить_кнопку(text, тип_обьекта="button", **атрибуты):
    """
    Создает кнопку.
    """
    кнопка = создать_элемент('button', type=тип_обьекта, **атрибуты)
    текст_узла = создать_текстовый_узел(text)
    добавить_элемент(кнопка, текст_узла)
    return кнопка

def добавить_текстовую_область(имя, строки=3, столбцы=50, **атрибуты):
    """
    Создает текстовую область.
    """
    return создать_элемент('textarea', name=имя, rows=строки, cols=столбцы, **атрибуты)

def добавить_выпадающий_список(имя, элементы, **атрибуты):
    """
    Создает выпадающий список.
    """
    select = создать_элемент('select', name=имя, **атрибуты)
    for элемент in элементы:
        option = создать_элемент('option', value=элемент)
        текст_узла = создать_текстовый_узел(элемент)
        добавить_элемент(option, текст_узла)
        добавить_элемент(select, option)
    return select

def добавить_метку(text, for_элемент=None, **атрибуты):
    """
    Создает метку.
    """
    метка = создать_элемент('label', **атрибуты)
    if for_элемент:
        метка.setAttribute('for', for_элемент)
    текст_узла = создать_текстовый_узел(text)
    добавить_элемент(метка, текст_узла)
    return метка

def добавить_разрыв_строки(**атрибуты):
    """
    Создает разрыв строки.
    """
    return создать_элемент('br', **атрибуты)

def добавить_горизонтальную_линию(**атрибуты):
    """
    Создает горизонтальную линию.
    """
    return создать_элемент('hr', **атрибуты)

def добавить_блок(**атрибуты):
    """
    Создает блок.
    """
    return создать_элемент('div', **атрибуты)

def добавить_спан(**атрибуты):
    """
    Создает span.
    """
    return создать_элемент('span', **атрибуты)

def добавить_цитату(текст, **атрибуты):
    """
    Создает цитату.
    """
    цитата = создать_элемент('blockquote', **атрибуты)
    текст_узла = создать_текстовый_узел(текст)
    добавить_элемент(цитата, текст_узла)
    return цитата

def добавить_подпись(текст, **атрибуты):
    """
    Создает подпись.
    """
    подпись = создать_элемент('figcaption', **атрибуты)
    текст_узла = создать_текстовый_узел(текст)
    добавить_элемент(подпись, текст_узла)
    return подпись

def добавить_фигуру(изображение, подпись=None, **атрибуты):
    """
    Создает фигуру.
    """
    фигура = создать_элемент('figure', **атрибуты)
    добавить_элемент(фигура, изображение)
    if подпись:
        добавить_элемент(фигура, подпись)
    return фигура

def добавить_видео(src, **атрибуты):
    """
    Создает видео.
    """
    return создать_элемент('video', src=src, **атрибуты)

def добавить_аудио(src, **атрибуты):
    """
    Создает аудио.
    """
    return создать_элемент('audio', src=src, **атрибуты)

def добавить_прогресс(значение_прогресса, максимум, **атрибуты):
    """
    Создает прогресс.
    """
    return создать_элемент('progress', value=значение, max=максимум, **атрибуты)

def добавить_метр(значение, минимум, максимум, **атрибуты):
    """
    Создает метр.
    """
    return создать_элемент('meter', value=значение_прогресса, min=минимум, max=максимум, **атрибуты)

def сохранить_сайт(имя_файла):
    """
    Сохраняет документ как валидный HTML5 файл.
    """
    global документ, html
    добавить_элемент(документ, html)
    html_str = документ.toprettyxml(indent="  ", encoding="UTF-8").decode("UTF-8")
    
    # Удаляем XML-декларацию
    html_str = html_str.replace('<?xml version="1.0" encoding="UTF-8"?>', '', 1)
    
    # Добавляем правильный DOCTYPE
    html_str = '<!DOCTYPE html>\n' + html_str
    
    # Убираем пустые строки
    html_str = "\n".join([line for line in html_str.split("\n") if line.strip()])
    
    # Добавляем расширение .html если нужно
    if not имя_файла.lower().endswith('.html'):
        имя_файла += '.html'
    
    # Сохраняем файл
    with open(имя_файла, 'w', encoding='utf-8') as файл:
        файл.write(html_str)

# Пример использования
#if __name__ == "__main__":
    # Инициализация документа
  #  создать_html()
  #  добавить_заголовок_страницы("Пример страницы")

    # Добавляем контент в body
   # добавить_элемент(body, добавить_заголовок(1, "Добро пожаловать!"))
  #  добавить_элемент(body, добавить_абзац("Это пример страницы с множеством элементов."))
    
    # Добавляем таблицу
   # таблица = добавить_таблицу([
   #     ["Ячейка 1", "Ячейка 2"],
   #     ["Ячейка 3", "Ячейка 4"]
  #  ], border="1")
 #   добавить_элемент(body, таблица)
    
    # Добавляем форму
  #  форма = добавить_форму(действие="/submit")
   # добавить_элемент(форма, добавить_поле_ввода(тип="text", имя="имя", placeholder="Введите имя"))
   # добавить_элемент(форма, добавить_кнопку(текст="Отправить", тип="submit"))
   # добавить_элемент(body, форма)
    
    # Сохраняем результат
  #  сохранить_в_файл("index.html")
