import re
import cmath

def производная(функция):
    """
    Функция для нахождения производной математической функции,
    заданной в виде строки. Использует стандартные операции и функции.
    """
    функция = функция.replace(" ", "")
    
    def deriv_term(term):
        """Вычисляет производную отдельного термина."""
        if term.isdigit():
            return "0"
        elif term == 'x':
            return "1"
        
        if term.startswith('sin('):
            return 'cos(' + term[4:-1] + ')'
        elif term.startswith('cos('):
            return '-' + 'sin(' + term[4:-1] + ')'
        elif term.startswith('tan('):
            return 'sec(' + term[4:-1] + ')**2'
        elif term.startswith('ln('):
            return '1/' + term[3:-1]
        elif term.startswith('e('):
            return 'e(' + term[2:-1] + ')'
        elif term.startswith('e**'):
            return 'e**(' + term[3:] + ')'
        
        if re.match(r'^x\*\*[0-9]+$', term):
            base, exponent = term.split('**')
            return f"{exponent}*{base}**{int(exponent) - 1}"

        if re.match(r'^[0-9]+(\.[0-9]+)?\*\*x$', term):
            base = term[:-3]
            return f"{term} * ln({base})"

        if '*' in term:
            factors = term.split('*')
            return ' + '.join(f'({deriv_term(factors[i])} * {" * ".join(factors[:i] + factors[i+1:])})' for i in range(len(factors)))

        elif '/' in term:
            numerator, denominator = term.split('/')
            return f'({deriv_term(numerator)} * {denominator} - {numerator} * {deriv_term(denominator)}) / {denominator}**2'

        return '0'  

    pattern = re.compile(r'(?<![a-zA-Z])([+-]?[^+-]+)')
    terms = pattern.findall(функция)

    производная_термина = [deriv_term(term) for term in terms if term]
    производная_термина = [t for t in производная_термина if t != "0"]
    
    if not производная_термина:
        return "0"
    
    производная_функции = '+'.join(производная_термина)
    производная_функции = производная_функции.replace('+-', '-').replace('++', '+').replace('-+', '-')

    return производная_функции

def неопределенный_интеграл(функция):
    """
    Функция для нахождения неопределенного интеграла математической функции,
    заданной в виде строки. Использует стандартные операции и функции.
    """
    функция = функция.replace(" ", "")
    
    def integ_term(term):
        """Вычисляет интеграл отдельного термина."""
        if term.isdigit():
            return f"{term}*x"
        elif term.isalpha() and len(term) == 1:
            return f"{term}**2/2"

        if term.startswith('sin('):
            return '-cos(' + term[4:-1] + ')'
        elif term.startswith('cos('):
            return 'sin(' + term[4:-1] + ')'
        elif term.startswith('tan('):
            return '-ln|cos(' + term[4:-1] + ')|'
        elif term.startswith('ln('):
            return f"{term[3:-1]}*ln({term[3:-1]}) - {term[3:-1]}"
        elif term.startswith('e('):
            return 'e(' + term[2:-1] + ')'
        elif term.startswith('e**'):
            return 'e**(' + term[3:] + ')'

        if '**' in term:
            base, exponent = term.split('**')
            exponent = int(exponent)
            if exponent == -1:
                return f'ln|{base}|'
            else:
                return f"{base}**{exponent + 1}/({exponent + 1})"

        return '0'

    pattern = re.compile(r'(?<![a-zA-Z])([+-]?[^+-]+)')
    terms = pattern.findall(функция)

    интеграл_термина = [integ_term(term) for term in terms if term]
    интеграл_функции = '+'.join(интеграл_термина) + ' + C'
    интеграл_функции = интеграл_функции.replace('+-', '-').replace('++', '+').replace('-+', '-')

    return интеграл_функции

def определенный_интеграл(функция, a, b):
    """
    Функция для нахождения численного интеграла заданной функции
    в интервале [a, b] с использованием метода трапеций.
    """
    
    def вычислить_значение(функция, x):
        """Вычисляет значение функции в точке x."""
        return eval(функция.replace('x', str(x)))

    n = 1000
    h = (b - a) / n
    интеграл_численный = 0.0

    for i in range(n):
        x_i = a + i * h
        x_next = a + (i + 1) * h
        интеграл_численный += (вычислить_значение(функция, x_i) + вычислить_значение(функция, x_next)) * h / 2

    return интеграл_численный

def предел(функция, x_0):
    """
    Функция для вычисления предела функции f(x) при x стремящемся к x_0.
    """
    eps = 1e-10
    try:
        limit_left = eval(функция.replace('x', str(x_0 - eps)))
        limit_right = eval(функция.replace('x', str(x_0 + eps)))
        
        if limit_left == limit_right:
            return limit_left
        else:
            return f"Предел не существует, так как значения разные: {limit_left} и {limit_right}"
    except Exception as e:
        return f"Ошибка при вычислении предела: {e}"
def мегакорень(число, основание):
    """
    Функция для вычисления корня по заданной степени.
    """
    return pow(число,1/основание)
def квадратное_уравнение(a, b, c):
    """
    Решает квадратное уравнение вида a*x^2 + b*x + c = 0.
    
    Параметры:
    a -- коэффициент при x^2
    b -- коэффициент при x
    c -- свободный член
    
    Возвращает:
    x -- корни уравнения или сообщение о количестве решений
    """
    if a == 0:
        return линейное_уравнение(b, c)  # Приводим к линейному уравнению
    
    дискриминант = b**2 - 4*a*c
    if дискриминант > 0:
        x1 = (-b + дискриминант**0.5) / (2*a)
        x2 = (-b - дискриминант**0.5) / (2*a)
        return (x1, x2)
    elif дискриминант == 0:
        x1 = -b / (2*a)
        return x1
    else:
        return 'Нет решений'

def линейное_уравнение(a, b):
    """
    Решает линейное уравнение вида a*x + b = 0.
    
    Параметры:
    a -- коэффициент при x
    b -- свободный член
    
    Возвращает:
    x -- корень уравнения или сообщение о количестве решений
    """
    if a == 0:
        if b == 0:
            return 'Бесконечно много решений'
        else:
            return 'Нет решений'
    x = -b / a
    return x

def линейное_неравенство(a, b, знак='>'):
    """
    Решает линейное неравенство вида a*x + b <, >, <=, >= 0.
    
    Параметры:
    a -- коэффициент при x
    b -- свободный член
    знак -- знак неравенства ('>', '<', '<=', '>=')

    Возвращает:
    x -- диапазон решений
    """
    if a == 0:
        if (знак == '>' and b > 0) or (знак == '>=' and b >= 0):
            return 'Все x'
        elif (знак == '<' and b < 0) or (знак == '<=' and b <= 0):
            return 'Нет решений'
        else:
            return 'Запрос некорректен'
    
    x = -b / a
    
    if знак == '>':
        return f'x > {x}'
    elif знак == '>=':
        return f'x >= {x}'
    elif знак == '<':
        return f'x < {x}'
    elif знак == '<=':
        return f'x <= {x}'
    else:
        return 'Запрос некорректен'

def квадратичное_неравенство(a, b, c, знак='>'):
    """
    Решает квадратичное неравенство вида a*x^2 + b*x + c <, >, <=, >= 0.
    
    Параметры:
    a -- коэффициент при x^2
    b -- коэффициент при x
    c -- свободный член
    знак -- знак неравенства ('>', '<', '<=', '>=')

    Возвращает:
    x -- диапазон решений
    """
    if a == 0:
        return линейное_неравенство(b, c, знак)  # Приводим к линейному неравенству

    корни = квадратное_уравнение(a, b, c)

    if корни == 'Нет решений':
        if a > 0:
            return 'a > 0, следовательно, x^2 + bx + c > 0 для всех x'
        else:
            return 'a < 0, следовательно, x^2 + bx + c < 0 для всех x'
    
    # Если корни вещественные
    if isinstance(корни, tuple):
        x1, x2 = корни
        if a > 0:
            if знак == '>':
                return f'x < {x1} или x > {x2}'
            elif знак == '>=':
                return f'x <= {x1} или x >= {x2}'
            elif знак == '<':
                return f'{x1} < x < {x2}'
            elif знак == '<=':
                return f'{x1} <= x <= {x2}'
            else:
                return 'Запрос некорректен'
        else:
            if знак == '>':
                return f'{x1} < x < {x2}'
            elif знак == '>=':
                return f'{x1} <= x <= {x2}'
            elif знак == '<':
                return f'x < {x1} или x > {x2}'
            elif знак == '<=':
                return f'x <= {x1} или x >= {x2}'
            else:
                return 'Запрос некорректен'
    else:
        return корни

def система_линейных_уравнений(a1, b1, c1, a2, b2, c2):
    """
    Решает систему линейных уравнений:
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    
    Параметры:
    a1, b1, c1 -- коэффициенты первого уравнения
    a2, b2, c2 -- коэффициенты второго уравнения
    
    Возвращает:
    (x, y) -- решение системы уравнений или сообщение о количестве решений
    """
    D = a1 * b2 - a2 * b1  # Определитель
    Dx = c1 * b2 - c2 * b1  # Определитель по x
    Dy = a1 * c2 - a2 * c1  # Определитель по y
    if D == 0:
        if Dx == 0 and Dy == 0:
            return 'Бесконечно много решений'  # Совпадающие прямые
        else:
            return 'Нет решений'  # Параллельные прямые
    x = Dx / D
    y = Dy / D
    return (x, y)

# Примеры использования функций
#print(квадратное_уравнение(1, -3, 2))  # Решает x^2 - 3x + 2 = 0
#print(линейное_уравнение(2, -4))  # Решает 2*x - 4 = 0
#print(линейное_неравенство(3, -9, '>'))  # Решает 3*x - 9 > 0
#print(квадратичное_неравенство(1, -3, 2, '>'))  # Решает x^2 - 3x + 2 > 0
#print(система_линейных_уравнений(1, 2, 3, 4, 5, 6))  # Решает систему уравнений

    
