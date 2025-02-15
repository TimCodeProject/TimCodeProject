import tkinter as tk
from tkinter import Listbox, Button, Toplevel, Scrollbar

class CommandApp:
    def __init__(self, root):
        self.root = root
        self.text_field = tk.Text(root, height=10, width=50)
        self.text_field.pack()

        self.commands = ["команда1", "команда2", "команда3", "команда4", "команда5"]

        self.button = tk.Button(root, text="Открыть команды", command=self.open_commands)
        self.button.pack()

    def open_commands(self):
        # Создаем новое окно
        command_window = Toplevel(self.root)
        command_window.title("Выбор команды")

        # Создаем Listbox для команд
        self.listbox = Listbox(command_window, height=10)
        for command in self.commands:
            self.listbox.insert(tk.END, command)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Создаем Scrollbar и связываем его с Listbox
        scrollbar = Scrollbar(command_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # Кнопка для вставки команды
        insert_button = Button(command_window, text="Вставить", command=self.insert_command)
        insert_button.pack()

    def insert_command(self):
        # Получаем выбранный элемент из Listbox
        selected_command = self.listbox.get(tk.ACTIVE)
        if selected_command:
            # Вставляем выбранную команду в текстовое поле
            self.text_field.insert(tk.END, selected_command + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandApp(root)
    root.mainloop()
