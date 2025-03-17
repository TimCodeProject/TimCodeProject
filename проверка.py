import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import io
import re
import random
import multiprocessing
import time
import string

def run_code(queue, code, input_data):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = sys.stderr = io.StringIO()
    
    try:
        if input_data:
            sys.stdin = io.StringIO('\n'.join(input_data))
        
        exec(code, {})
        output = sys.stdout.getvalue().splitlines()
        error = None
    except Exception as e:
        output = None
        error = str(e)
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    queue.put((output, error))

def apply_modern_theme(root):
    style = ttk.Style()
    style.theme_use('clam')
    
    bg_color = "#f0f0f0"
    fg_color = "#000000"
    accent_color = "#ffffff"
    highlight_color = "#e0e0e0"
    
    style.configure(".", 
        background=bg_color, 
        foreground=fg_color,
        font=('Helvetica', 10)
    )
    
    style.map('TCombobox',
        fieldbackground=[('readonly', accent_color)],
        foreground=[('readonly', fg_color)]
    )
    
    style.configure('TListbox', 
        background=accent_color,
        foreground=fg_color,
        selectbackground=highlight_color
    )
    
    root.configure(bg=bg_color)
    root.option_add('*Listbox*Background', accent_color)
    root.option_add('*Listbox*Foreground', fg_color)
    root.option_add('*Listbox*selectBackground', highlight_color)

class CodeCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Проверка олимпиадных заданий")
        self.geometry("1400x900")
        apply_modern_theme(self)
        
        self.create_widgets()
        self.custom_test_inputs = []
        
    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="Проверка")
        self.create_code_editors(main_tab)
        
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="Настройки")
        self.create_settings_panel(settings_tab)

    def create_code_editors(self, parent):
        code_panel = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        code_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.check_code_editor = self.create_editor(code_panel, "Код проверки (эталонный):")
        self.participant_code_editor = self.create_editor(code_panel, "Код участника:")
        
        self.run_button = ttk.Button(parent, text="Запустить проверку", command=self.run_tests)
        self.run_button.pack(pady=10)
        
        self.results_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, height=15)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_editor(self, parent, label_text):
        frame = ttk.Frame(parent)
        label = ttk.Label(frame, text=label_text)
        label.pack(anchor='w')
        editor = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15)
        editor.pack(fill=tk.BOTH, expand=True)
        parent.add(frame)
        return editor

    def create_settings_panel(self, parent):
        settings_frame = ttk.Frame(parent)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_test_settings(settings_frame)
        self.create_custom_tests(settings_frame)

    def create_test_settings(self, parent):
        settings_frame = ttk.LabelFrame(parent, text="Настройки тестирования")
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        time_frame = ttk.Frame(settings_frame)
        time_frame.pack(fill=tk.X, pady=5)
        ttk.Label(time_frame, text="Лимит времени (сек):").pack(side=tk.LEFT)
        self.time_limit_entry = ttk.Spinbox(time_frame, from_=0.1, to=60, increment=0.5)
        self.time_limit_entry.set(1)
        self.time_limit_entry.pack(side=tk.LEFT, padx=5)

        points_frame = ttk.Frame(settings_frame)
        points_frame.pack(fill=tk.X, pady=5)
        ttk.Label(points_frame, text="Баллы за тест:").pack(side=tk.LEFT)
        self.points_entry = ttk.Spinbox(points_frame, from_=1, to=10, increment=1)
        self.points_entry.set(2)
        self.points_entry.pack(side=tk.LEFT, padx=5)

        self.create_test_generator(settings_frame)

    def create_test_generator(self, parent):

        gen_frame = ttk.LabelFrame(parent, text="Генератор тестов")
        gen_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        # Новая настройка - метод ввода
        input_method_frame = ttk.Frame(gen_frame)
        input_method_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_method_frame, text="Метод ввода:").pack(side=tk.LEFT)
        self.input_method = ttk.Combobox(input_method_frame, values=["Стандартный", "Линейный"])
        self.input_method.current(0)
        self.input_method.pack(side=tk.LEFT, padx=5)
    
        self.delimiter_entry = ttk.Entry(input_method_frame, width=5)
        self.delimiter_entry.insert(0, ",")
        self.delimiter_entry.pack(side=tk.LEFT, padx=5)
        self.delimiter_entry.config(state='disabled')  # По умолчанию отключено
    
        # Привязываем изменение метода ввода к обновлению состояния поля разделителя
        self.input_method.bind("<<ComboboxSelected>>", self.update_delimiter_state)

        # Новая настройка - количество вводов на тест
        input_count_frame = ttk.Frame(gen_frame)
        input_count_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_count_frame, text="Вводов на тест:").pack(side=tk.LEFT)
        self.inputs_per_test = ttk.Spinbox(input_count_frame, from_=1, to=100, increment=1)
        self.inputs_per_test.set(1)
        self.inputs_per_test.pack(side=tk.LEFT, padx=5)

        type_frame = ttk.Frame(gen_frame)
        type_frame.pack(fill=tk.X, pady=5)
        ttk.Label(type_frame, text="Тип данных:").pack(side=tk.LEFT)
        self.data_type = ttk.Combobox(type_frame, values=[
            "Целые числа", 
            "Дробные числа",
            "Строки",
            "Смешанные"
        ])
        self.data_type.current(0)
        self.data_type.pack(side=tk.LEFT, padx=5)
        self.data_type.bind("<<ComboboxSelected>>", self.update_settings_visibility)
        
        self.int_settings_frame = ttk.LabelFrame(gen_frame, text="Настройки целых чисел")
        self.min_int_entry = ttk.Spinbox(self.int_settings_frame, from_=-100000, to=100000, increment=1)
        self.min_int_entry.set(-1000)
        self.max_int_entry = ttk.Spinbox(self.int_settings_frame, from_=-100000, to=100000, increment=1)
        self.max_int_entry.set(1000)
        ttk.Label(self.int_settings_frame, text="Минимум:").pack(side=tk.LEFT, padx=5)
        self.min_int_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.int_settings_frame, text="Максимум:").pack(side=tk.LEFT, padx=5)
        self.max_int_entry.pack(side=tk.LEFT, padx=5)

        self.float_settings_frame = ttk.LabelFrame(gen_frame, text="Настройки дробных чисел")
        self.min_float_entry = ttk.Spinbox(self.float_settings_frame, from_=-100000.0, to=100000.0, increment=1.0)
        self.min_float_entry.set(-100.0)
        self.max_float_entry = ttk.Spinbox(self.float_settings_frame, from_=-100000.0, to=100000.0, increment=1.0)
        self.max_float_entry.set(100.0)
        self.precision_entry = ttk.Spinbox(self.float_settings_frame, from_=0, to=10, increment=1)
        self.precision_entry.set(2)
        ttk.Label(self.float_settings_frame, text="Минимум:").pack(side=tk.LEFT, padx=5)
        self.min_float_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.float_settings_frame, text="Максимум:").pack(side=tk.LEFT, padx=5)
        self.max_float_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.float_settings_frame, text="Точность:").pack(side=tk.LEFT, padx=5)
        self.precision_entry.pack(side=tk.LEFT, padx=5)

        self.string_settings_frame = ttk.LabelFrame(gen_frame, text="Настройки строк")
        self.string_length_entry = ttk.Spinbox(self.string_settings_frame, from_=1, to=1000, increment=1)
        self.string_length_entry.set(5)
        self.string_chars_entry = ttk.Entry(self.string_settings_frame)
        ttk.Label(self.string_settings_frame, text="Длина:").pack(side=tk.LEFT, padx=5)
        self.string_length_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.string_settings_frame, text="Символы:").pack(side=tk.LEFT, padx=5)
        self.string_chars_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        count_frame = ttk.Frame(gen_frame)
        count_frame.pack(fill=tk.X, pady=5)
        ttk.Label(count_frame, text="Количество тестов:").pack(side=tk.LEFT)
        self.test_count = ttk.Spinbox(count_frame, from_=1, to=1000, increment=1)
        self.test_count.set(50)
        self.test_count.pack(side=tk.LEFT, padx=5)

        gen_btn = ttk.Button(gen_frame, text="Сгенерировать", command=self.generate_test_inputs)
        gen_btn.pack(pady=5)
        
        self.update_settings_visibility()

    def update_settings_visibility(self, event=None):
        selected_type = self.data_type.get()
        self.int_settings_frame.pack_forget()
        self.float_settings_frame.pack_forget()
        self.string_settings_frame.pack_forget()
        
        if selected_type == "Целые числа":
            self.int_settings_frame.pack(fill=tk.X, pady=5)
        elif selected_type == "Дробные числа":
            self.float_settings_frame.pack(fill=tk.X, pady=5)
        elif selected_type == "Строки":
            self.string_settings_frame.pack(fill=tk.X, pady=5)
        elif selected_type == "Смешанные":
            self.int_settings_frame.pack(fill=tk.X, pady=5)
            self.float_settings_frame.pack(fill=tk.X, pady=5)
            self.string_settings_frame.pack(fill=tk.X, pady=5)

    def create_custom_tests(self, parent):
        custom_frame = ttk.LabelFrame(parent, text="Пользовательские тесты")
        custom_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        input_frame = ttk.Frame(custom_frame)
        input_frame.pack(fill=tk.X, pady=5)
        self.test_input_editor = scrolledtext.ScrolledText(input_frame, height=3)
        self.test_input_editor.pack(fill=tk.X)

        btn_frame = ttk.Frame(custom_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        add_btn = ttk.Button(btn_frame, text="Добавить", command=self.add_custom_test)
        add_btn.pack(side=tk.LEFT)
        del_btn = ttk.Button(btn_frame, text="Удалить", command=self.remove_custom_test)
        del_btn.pack(side=tk.LEFT)

        self.custom_tests_list = tk.Listbox(custom_frame)
        self.custom_tests_list.pack(fill=tk.BOTH, expand=True)

    def translate_code(self, code):
        replacements = {
            'ввод': 'input',
            'вывод': 'print',
            'равно': '==',
            'неравно': '!=',
            'больше': '>',
            'меньше': '<',
            'больше_равно': '>=',
            'меньше_равно': '<=',
            'и': 'and',
            'или': 'or',
            'не': 'not',
            'Правда': 'True',
            'Ложь': 'False',
            'если': 'if',
            'иначе': 'else',
            'пока': 'while',
            'для': 'for',
            'попробовать': 'try',
            'кроме': 'except',
            'вернуть': 'return'
        }
        pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in replacements.keys()) + r')\b')
        return pattern.sub(lambda x: replacements[x.group()], code)

    def add_custom_test(self):
        # Получаем данные из редактора
        input_data = self.test_input_editor.get("1.0", tk.END).strip().split('\n')
    
        if input_data:
            # Добавляем новый тест в список
            self.custom_test_inputs.append(input_data)
        
            # Определяем метод ввода
            input_method = self.input_method.get()
        
            # Формируем отображаемый ввод
            if input_method == "Линейный":
                delimiter = self.delimiter_entry.get()
                display_input = delimiter.join(input_data)
            else:
                display_input = '\n'.join(input_data)
        
            # Добавляем тест в список отображения
            test_number = len(self.custom_test_inputs)
            self.custom_tests_list.insert(tk.END, f"Тест {test_number}: Ввод: {display_input}")
        
            # Очищаем редактор ввода
            self.test_input_editor.delete("1.0", tk.END)
            

    def remove_custom_test(self):
        selected = self.custom_tests_list.curselection()
        if selected:
            index = selected[0]
            self.custom_tests_list.delete(index)
            del self.custom_test_inputs[index]

    def execute_code(self, code, input_data=None, time_limit=None):
        if time_limit is None:
            time_limit = float(self.time_limit_entry.get())
        
        queue = multiprocessing.Queue()
        translated_code = self.translate_code(code)
        process = multiprocessing.Process(target=run_code, args=(queue, translated_code, input_data))
        process.start()
        process.join(time_limit)
        
        if process.is_alive():
            process.terminate()
            process.join()
            return None, "Превышено время выполнения"
        
        return queue.get() if not queue.empty() else (None, "Ошибка выполнения")

    # Добавляем метод для обновления состояния поля разделителя
    def update_delimiter_state(self, event=None):
        if self.input_method.get() == "Линейный":
            self.delimiter_entry.config(state='normal')
        else:
            self.delimiter_entry.config(state='disabled')

    def generate_test_inputs(self):
        data_type = self.data_type.get()
        test_inputs = []
        test_count = int(self.test_count.get())
        inputs_per_test = int(self.inputs_per_test.get())
        input_method = self.input_method.get()
        delimiter = self.delimiter_entry.get() if input_method == "Линейный" else None
    
        if data_type == "Целые числа":
            min_val = int(self.min_int_entry.get())
            max_val = int(self.max_int_entry.get())
            inputs = [
                [str(random.randint(min_val, max_val)) for _ in range(inputs_per_test)] 
                for _ in range(test_count)
            ]
        
        elif data_type == "Дробные числа":
            min_val = float(self.min_float_entry.get())
            max_val = float(self.max_float_entry.get())
            precision = int(self.precision_entry.get())
            inputs = [
                [f"{round(random.uniform(min_val, max_val), precision):.{precision}f}" 
                 for _ in range(inputs_per_test)] 
                for _ in range(test_count)
            ]
        
        elif data_type == "Строки":
            length = int(self.string_length_entry.get())
            chars = self.string_chars_entry.get().strip() or string.printable
            chars = list(chars) if isinstance(chars, str) else chars  # Преобразуем chars в список
            inputs = [
                [''.join(random.choices(chars, k=length)) for _ in range(inputs_per_test)] 
                for _ in range(test_count)
            ]
        
        elif data_type == "Смешанные":
            min_int = int(self.min_int_entry.get())
            max_int = int(self.max_int_entry.get())
            min_float = float(self.min_float_entry.get())
            max_float = float(self.max_float_entry.get())
            precision = int(self.precision_entry.get())
            str_length = int(self.string_length_entry.get())
            str_chars = self.string_chars_entry.get().strip() or string.printable
            str_chars = list(str_chars) if isinstance(str_chars, str) else str_chars  # Преобразуем chars в список
        
            inputs = []
            for _ in range(test_count):
                test_input = []
                for _ in range(inputs_per_test):
                    data_type = random.choice(['int', 'float', 'string'])
                    if data_type == 'int':
                        test_input.append(str(random.randint(min_int, max_int)))
                    elif data_type == 'float':
                        value = round(random.uniform(min_float, max_float), precision)
                        test_input.append(f"{value:.{precision}f}")
                    else:
                        test_input.append(''.join(random.choices(str_chars, k=str_length)))
                inputs.append(test_input)
    
    # Применяем метод ввода
        if input_method == "Линейный":
            test_inputs = [[delimiter.join(map(str, test))] for test in inputs]
        else:
            test_inputs = inputs
    
        self.custom_test_inputs = test_inputs
        self.custom_tests_list.delete(0, tk.END)
        for i, inp in enumerate(test_inputs, 1):
            display_input = ', '.join(map(str, inp[0])) if input_method == "Линейный" else '\n'.join(map(str, inp))
            self.custom_tests_list.insert(tk.END, f"Тест {i}: Ввод: {display_input}")
        

    def run_tests(self):
        check_code = self.check_code_editor.get("1.0", tk.END)
        participant_code = self.participant_code_editor.get("1.0", tk.END)
        
        if not self.custom_test_inputs:
            messagebox.showwarning("Предупреждение", "Нет тестов для выполнения!")
            return
        
        total_score = 0
        points_per_test = int(self.points_entry.get())
        max_score = len(self.custom_test_inputs) * points_per_test
        time_limit = float(self.time_limit_entry.get())
        
        self.results_text.delete(1.0, tk.END)
        
        for i, input_data in enumerate(self.custom_test_inputs, 1):
            ref_output, ref_error = self.execute_code(check_code, input_data, time_limit)
            if ref_error:
                self.results_text.insert(tk.END, 
                    f"Тест {i}: Ошибка в эталонном коде ❌\n{ref_error}\n\n")
                continue
                
            part_output, part_error = self.execute_code(participant_code, input_data, time_limit)
            
            result_line = f"Тест {i}: Ввод: {input_data}\n"
            if part_error:
                result_line += f"Ошибка выполнения ❌\n{part_error}\n"
            elif part_output == ref_output:
                total_score += points_per_test
                result_line += f"Успешно ✅\n"
            else:
                result_line += (f"Неудачно ❌\nОжидалось: {ref_output}\nПолучено: {part_output}\n")
            
            self.results_text.insert(tk.END, result_line + "\n")
            self.results_text.yview(tk.END)
            self.update()
        
        self.results_text.insert(tk.END, 
            f"\nИтоговый результат: {total_score}/{max_score} баллов")

if __name__ == "__main__":
    app = CodeCheckerApp()
    app.mainloop()
