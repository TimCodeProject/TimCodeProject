import tkinter as tk
from tkinter import ttk

class CustomMenuExample:
    def __init__(self, root):
        self.root = root
        self.root.title("Пример меню с виджетами")
        
        # Создаем главное меню
        self.menu_bar = tk.Menu(root)
        
        # Вкладка "Инструменты"
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Инструменты", menu=self.tools_menu)
        
        # Добавляем элементы в меню
        # 1. Чекбокс
        self.check_var = tk.BooleanVar()
        self.tools_menu.add_checkbutton(
            label="Чекбокс", 
            variable=self.check_var,
            command=self.on_checkbox_toggle
        )
        
        # 2. Кнопка
        self.tools_menu.add_command(
            label="Кнопка", 
            command=self.on_button_click
        )
        
        # 3. Радиокнопки
        self.radio_var = tk.StringVar()
        self.tools_menu.add_radiobutton(
            label="Вариант 1", 
            variable=self.radio_var, 
            value="1",
            command=self.on_radio_change
        )
        self.tools_menu.add_radiobutton(
            label="Вариант 2", 
            variable=self.radio_var, 
            value="2",
            command=self.on_radio_change
        )
        
        # 4. Комбобокс (используем кастомное подменю)
        self.combo_submenu = tk.Menu(self.tools_menu, tearoff=0)
        self.combo_var = tk.StringVar()
        self.combo_submenu.add_radiobutton(label="Опция 1", variable=self.combo_var, value="1")
        self.combo_submenu.add_radiobutton(label="Опция 2", variable=self.combo_var, value="2")
        self.combo_submenu.add_radiobutton(label="Опция 3", variable=self.combo_var, value="3")
        self.tools_menu.add_cascade(label="Комбобокс", menu=self.combo_submenu)
        
        # 5. Ползунок (кастомное всплывающее окно)
        self.tools_menu.add_command(
            label="Ползунок", 
            command=self.show_slider_popup
        )
        
        # 6. Разделитель
        self.tools_menu.add_separator()
        
        # Устанавливаем меню в окно
        self.root.config(menu=self.menu_bar)
        
        # Текстовое поле для вывода информации
        self.text = tk.Text(root, height=10, width=40)
        self.text.pack(pady=10)
    
    def on_checkbox_toggle(self):
        state = "ВКЛ" if self.check_var.get() else "ВЫКЛ"
        self.text.insert(tk.END, f"Чекбокс: {state}\n")
    
    def on_button_click(self):
        self.text.insert(tk.END, "Кнопка нажата!\n")
    
    def on_radio_change(self):
        self.text.insert(tk.END, f"Выбран вариант: {self.radio_var.get()}\n")
    
    def show_slider_popup(self):
        # Создаем всплывающее окно с ползунком
        popup = tk.Toplevel()
        popup.title("Ползунок")
        
        slider = ttk.Scale(
            popup,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=lambda v: self.text.insert(tk.END, f"Значение ползунка: {float(v):.1f}\n")
        )
        slider.pack(padx=20, pady=10)
        
        ttk.Button(popup, text="Закрыть", command=popup.destroy).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomMenuExample(root)
    root.mainloop()
