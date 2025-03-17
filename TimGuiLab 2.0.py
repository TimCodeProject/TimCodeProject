import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import re

class DraggableButton:
    def __init__(self, canvas, x, y, text="Кнопка"):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+100, y+40, fill="#e1e1e1", outline="#999")
        self.text_id = canvas.create_text(x+50, y+20, text=text, fill="black")
        
        self.properties = {
            "x": x,
            "y": y,
            "width": 100,
            "height": 40,
            "text": text,
            "bg_color": "#e1e1e1",
            "text_color": "black",
            "command": ""
        }
        
        self.canvas.tag_bind(self.id, '<Button-1>', self.start_move)
        self.canvas.tag_bind(self.id, '<B1-Motion>', self.move)
        self.canvas.tag_bind(self.text_id, '<Button-1>', self.start_move)
        self.canvas.tag_bind(self.text_id, '<B1-Motion>', self.move)
        
        self.canvas.tag_bind(self.id, '<Button-3>', self.start_resize)
        self.canvas.tag_bind(self.id, '<B3-Motion>', self.resize)
        self.canvas.tag_bind(self.text_id, '<Button-3>', self.start_resize)
        self.canvas.tag_bind(self.text_id, '<B3-Motion>', self.resize)

    def start_move(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.master.select_button(self)

    def move(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)
        self.properties["x"] += dx
        self.properties["y"] += dy
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.master.update_properties(self)

    def start_resize(self, event):
        self.start_width = self.properties["width"]
        self.start_height = self.properties["height"]
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.master.select_button(self)

    def resize(self, event):
        dw = event.x - self.start_x
        dh = event.y - self.start_y
        new_width = max(50, self.start_width + dw)
        new_height = max(20, self.start_height + dh)
        
        self.canvas.coords(self.id, 
            self.properties["x"],
            self.properties["y"],
            self.properties["x"] + new_width,
            self.properties["y"] + new_height
        )
        self.canvas.coords(self.text_id,
            self.properties["x"] + new_width/2,
            self.properties["y"] + new_height/2
        )
        self.properties["width"] = new_width
        self.properties["height"] = new_height
        self.canvas.master.update_properties(self)

    def update_properties(self, props):
        self.properties = props
        self.canvas.itemconfig(self.id, fill=props["bg_color"])
        self.canvas.itemconfig(self.text_id, text=props["text"], fill=props["text_color"])
        self.canvas.coords(self.id, 
            props["x"], props["y"],
            props["x"] + props["width"],
            props["y"] + props["height"]
        )
        self.canvas.coords(self.text_id,
            props["x"] + props["width"]/2,
            props["y"] + props["height"]/2
        )

class EditorTab(ttk.Frame):
    def __init__(self, master, code_callback):
        super().__init__(master)
        self.code_callback = code_callback
        self.current_button = None
        self.buttons = []
        self.attribute_translation = {
    "width": "ширина",
    "height": "высота",
    "text": "текст",
    "bg_color": "цвет_фона",
    "text_color": "цвет_текста",
    "command": "команда"
}
        
        # Canvas для размещения кнопок
        self.canvas = tk.Canvas(self, bg="white", cursor="crosshair")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Панель свойств
        self.props_frame = ttk.LabelFrame(self, text="Свойства")
        self.props_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Элементы управления свойствами
        ttk.Button(self.props_frame, text="Создать кнопку", command=self.create_button).pack(pady=5)
        
        self.prop_widgets = {}
        properties = [
            ("width", "Ширина:"),
            ("height", "Высота:"),
            ("text", "Текст:"),
            ("bg_color", "Цвет фона:"),
            ("text_color", "Цвет текста:"),
            ("command", "Команда:")
        ]
        
        for prop, label in properties:
            frame = ttk.Frame(self.props_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label, width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            if "color" in prop:
                btn = ttk.Button(frame, text="...", width=3, 
                               command=lambda p=prop: self.choose_color(p))
                btn.pack(side=tk.LEFT, padx=2)
            entry.bind("<FocusOut>", self.update_from_property)
            self.prop_widgets[prop] = entry

    def create_button(self):
        new_btn = DraggableButton(self.canvas, 50, 50)
        self.buttons.append(new_btn)
        self.select_button(new_btn)

    def select_button(self, button):
        self.current_button = button
        for prop, widget in self.prop_widgets.items():
            widget.delete(0, tk.END)
            widget.insert(0, str(button.properties[prop]))
        self.generate_code()

    def update_properties(self, button):
        if self.current_button == button:
            for prop, widget in self.prop_widgets.items():
                widget.delete(0, tk.END)
                widget.insert(0, str(button.properties[prop]))
        self.generate_code()

    def update_from_property(self, event):
        if not self.current_button:
            return
            
        props = self.current_button.properties.copy()
        for prop, widget in self.prop_widgets.items():
            try:
                if prop in ["x", "y", "width", "height"]:
                    props[prop] = int(widget.get())
                else:
                    props[prop] = widget.get()
            except:
                pass
        
        self.current_button.update_properties(props)
        self.generate_code()

    def choose_color(self, prop):
        color = colorchooser.askcolor()[1]
        if color:
            self.prop_widgets[prop].delete(0, tk.END)
            self.prop_widgets[prop].insert(0, color)
            self.update_from_property(None)

    def generate_code(self):
        code = ""
        code += 'использовать графический_интерфейс как гип\n'
        code +=f'окно = гип.Окно()\n'
        for button in self.buttons:
            # Генерируем строку для создания виджета без координат
            code += f"{'виджет' + str(self.buttons.index(button) + 1)} = гип.Кнопка(окно,\n"
            for prop, value in button.properties.items():
                if prop not in ["x", "y", "width","height"]:  # Исключаем координаты
                    translated_prop = self.attribute_translation.get(prop, prop)  # Переводим атрибут
                    code += f"    {translated_prop}={repr(value)},\n"
            code += ")\n"

            # Добавляем строку для установки координат
            code += f"виджет{self.buttons.index(button) + 1}.поставить(x={button.properties['x']}, y={button.properties['y']}, ширина={button.properties['width']},высота={button.properties['height']})\n\n"
        code += 'окно.главный_цикл()'
        self.code_callback(code)


    def load_from_code(self, code):
        self.buttons.clear()  # Очистка предыдущих кнопок
        self.canvas.delete("all")  # Очистка канваса

        # Разделяем код на строки
        lines = code.strip().splitlines()
    
        # Проверяем, что код не пуст
        if not lines:
            messagebox.showerror("Ошибка", "Файл пуст")
            return  

        # Проверяем, что файл начинается с правильной строки
        if not lines[0].startswith('использовать графический_интерфейс как гип'):
            messagebox.showerror("Ошибка", "Неверный формат файла")
            return

        current_button = None
        params = {}
    
        for line in lines:
            line = line.strip()
        
            # Игнорируем пустые строки
            if not line:
                continue
        
            # Проверка на создание кнопки
            button_match = re.match(r'^(виджет\d+)\s*=\s*гип\.Кнопка$$$(.*)$$$$', line)
            if button_match:
                button_name, args = button_match.groups()
                current_button = DraggableButton(self.canvas, 0, 0)  # Создаем кнопку с нулевыми координатами
                params = {}  # Сбрасываем параметры для новой кнопки
                continue

            # Проверка на параметры кнопки
            param_match = re.match(r'(\w+)\s*=\s*(.+)', line)
            if param_match and current_button:
                key, value = param_match.groups()
                params[key] = value.strip().strip('"').strip("'")  # Удаляем кавычки

            if current_button and line.startswith(f'{button_name}.поставить'):
                position_match = re.match(rf'{button_name}\.поставить$$$\s*x\s*=\s*(\d+),\s*y\s*=\s*(\d+),\s*ширина\s*=\s*(\d+),\s*высота\s*=\s*(\d+)\s*$$$', line)
                if position_match:
                    x, y, width, height = map(int, position_match.groups())
                    current_button.properties['x'] = x
                    current_button.properties['y'] = y
                    current_button.properties['width'] = width
                    current_button.properties['height'] = height
                
                    # Обновляем виджет
                    current_button.update_properties(current_button.properties)
                    self.buttons.append(current_button)  # Добавляем кнопку в список
                    current_button = None  # Сбрасываем текущую кнопку для следующей
                    continue

        # Обновляем канвас, чтобы отобразить кнопки
        for button in self.buttons:
            button.update_properties(button.properties)

                                      

class CodeTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.text = tk.Text(self, wrap=tk.WORD, font=("Courier", 12), 
                          bg="#1e1e1e", fg="white", insertbackground="white")
        scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

class TimGuiLab(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TimGuiLab")
        self.geometry("1200x800")
        
        # Настройка меню
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Новый", command = self.new_file)
        file_menu.add_command(label="Открыть", command= self.open_file)
        file_menu.add_command(label="Сохранить", command= self.save_file)
        self.menu.add_cascade(label="Файл", menu=file_menu)
        
        # Настройка вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка редактора
        self.editor_tab = EditorTab(self.notebook, self.update_code)
        self.notebook.add(self.editor_tab, text="Визуальный редактор")
        
        # Вкладка кода
        self.code_tab = CodeTab(self.notebook)
        self.notebook.add(self.code_tab, text="Редактор кода")

    def new_file(self):
        self.editor_tab.buttons.clear()
        self.editor_tab.code_callback("")  # Очистить код
        self.editor_tab.canvas.delete("all")  # Очистить канвас

    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension=".txt", 
                                                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                code = file.read()
                self.editor_tab.load_from_code(code)

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                  filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(self.code_tab.text.get("1.0", tk.END))        

    def update_code(self, code):
        self.code_tab.text.delete("1.0", tk.END)
        self.code_tab.text.insert("1.0", code)

if __name__ == "__main__":
    app = TimGuiLab()
    app.mainloop()
