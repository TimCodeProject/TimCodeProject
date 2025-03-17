import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import telebot
import threading
from PIL import Image, ImageTk

# Основной класс приложения
class TelegramBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конструктор Telegram ботов")
        self.root.geometry("1000x800")
        self.bot = None
        self.bot_token = None
        self.commands = {}
        self.keyboards = {}
        self.variables = {}
        self.dark_theme = False

        # Переменные для хранения данных
        self.bot_token_var = tk.StringVar()
        self.command_name_var = tk.StringVar()
        self.command_response_var = tk.StringVar()
        self.keyboard_name_var = tk.StringVar()
        self.keyboard_buttons_var = tk.StringVar()
        self.variable_name_var = tk.StringVar()
        self.variable_value_var = tk.StringVar()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Верхняя панель
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top_frame, text="Токен бота:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.bot_token_var, width=50).pack(side=tk.LEFT, padx=10)
        ttk.Button(top_frame, text="Подключить", command=self.connect_bot).pack(side=tk.LEFT)

        # Кнопка переключения темы
        ttk.Button(top_frame, text="Темная тема", command=self.toggle_theme).pack(side=tk.RIGHT)

        # Панель добавления команд
        command_frame = ttk.LabelFrame(self.root, text="Добавить команду")
        command_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(command_frame, text="Имя команды:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(command_frame, textvariable=self.command_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(command_frame, text="Ответ команды:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(command_frame, textvariable=self.command_response_var).grid(row=1, column=1, padx=5, pady=5)

        # Выбор поведения бота
        ttk.Label(command_frame, text="Поведение бота:").grid(row=2, column=0, padx=5, pady=5)
        self.behavior_var = tk.StringVar(value="text")  # По умолчанию - текстовый ответ
        ttk.Radiobutton(command_frame, text="Текстовый ответ", variable=self.behavior_var, value="text").grid(row=2, column=1, padx=5, pady=5)
        ttk.Radiobutton(command_frame, text="Отправить фото", variable=self.behavior_var, value="photo").grid(row=3, column=1, padx=5, pady=5)
        ttk.Radiobutton(command_frame, text="Отправить клавиатуру", variable=self.behavior_var, value="keyboard").grid(row=4, column=1, padx=5, pady=5)

        ttk.Button(command_frame, text="Добавить команду", command=self.add_command).grid(row=5, column=0, columnspan=2, pady=5)

        # Панель создания клавиатур
        keyboard_frame = ttk.LabelFrame(self.root, text="Создать клавиатуру")
        keyboard_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(keyboard_frame, text="Название клавиатуры:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(keyboard_frame, textvariable=self.keyboard_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(keyboard_frame, text="Кнопки (через запятую):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(keyboard_frame, textvariable=self.keyboard_buttons_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(keyboard_frame, text="Создать клавиатуру", command=self.create_keyboard).grid(row=2, column=0, columnspan=2, pady=5)

        # Панель работы с переменными
        variable_frame = ttk.LabelFrame(self.root, text="Управление переменными")
        variable_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(variable_frame, text="Имя переменной:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(variable_frame, textvariable=self.variable_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(variable_frame, text="Значение переменной:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(variable_frame, textvariable=self.variable_value_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(variable_frame, text="Добавить переменную", command=self.add_variable).grid(row=2, column=0, columnspan=2, pady=5)

        # Панель работы с файлами
        file_frame = ttk.LabelFrame(self.root, text="Работа с файлами")
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(file_frame, text="Загрузить файл", command=self.upload_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Загрузить фото", command=self.upload_photo).pack(side=tk.LEFT, padx=5)

        # Панель симуляции мессенджера
        messenger_frame = ttk.LabelFrame(self.root, text="Симуляция мессенджера")
        messenger_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.messenger_text = tk.Text(messenger_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.messenger_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Поле ввода команд
        input_frame = ttk.Frame(messenger_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Отправить", command=self.send_command).pack(side=tk.LEFT)

    def connect_bot(self):
        self.bot_token = self.bot_token_var.get()
        if not self.bot_token:
            messagebox.showerror("Ошибка", "Введите токен бота!")
            return

        try:
            self.bot = telebot.TeleBot(self.bot_token)
            messagebox.showinfo("Успех", "Бот подключен!")
            self.start_bot()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться: {e}")

    def start_bot(self):
        def bot_polling():
            self.bot.polling(none_stop=True)

        bot_thread = threading.Thread(target=bot_polling)
        bot_thread.daemon = True
        bot_thread.start()

    def add_command(self):
        command_name = self.command_name_var.get()
        command_response = self.command_response_var.get()
        behavior = self.behavior_var.get()

        if not command_name or (not command_response and behavior != "keyboard"):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        self.commands[command_name] = {
            "response": command_response,
            "behavior": behavior
        }

        @self.bot.message_handler(commands=[command_name])
        def handle_command(message):
            if behavior == "text":
                self.bot.reply_to(message, command_response)
            elif behavior == "photo":
                self.bot.send_photo(message.chat.id, open(command_response, "rb"))
            elif behavior == "keyboard":
                keyboard_name = command_response
                if keyboard_name in self.keyboards:
                    self.bot.send_message(message.chat.id, "Выберите действие:", reply_markup=self.keyboards[keyboard_name])

        self.update_messenger(f"Добавлена команда: /{command_name}", "system")
        messagebox.showinfo("Успех", f"Команда '{command_name}' добавлена!")

    def create_keyboard(self):
        keyboard_name = self.keyboard_name_var.get()
        buttons = self.keyboard_buttons_var.get().split(",")

        if not keyboard_name or not buttons:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        for button in buttons:
            markup.add(telebot.types.KeyboardButton(button.strip()))

        self.keyboards[keyboard_name] = markup
        self.update_messenger(f"Создана клавиатура: {keyboard_name}", "system")
        messagebox.showinfo("Успех", f"Клавиатура '{keyboard_name}' создана!")

    def add_variable(self):
        variable_name = self.variable_name_var.get()
        variable_value = self.variable_value_var.get()

        if not variable_name or not variable_value:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        self.variables[variable_name] = variable_value
        self.update_messenger(f"Добавлена переменная: {variable_name} = {variable_value}", "system")
        messagebox.showinfo("Успех", f"Переменная '{variable_name}' добавлена!")

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                self.bot.send_document(self.bot_token, file)
            self.update_messenger(f"Файл отправлен: {file_path}", "system")
            messagebox.showinfo("Успех", "Файл отправлен!")

    def upload_photo(self):
        photo_path = filedialog.askopenfilename()
        if photo_path:
            with open(photo_path, "rb") as photo:
                self.bot.send_photo(self.bot_token, photo)
            self.update_messenger(f"Фото отправлено: {photo_path}", "system")
            messagebox.showinfo("Успех", "Фото отправлено!")

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        theme = "dark" if self.dark_theme else "light"
        self.root.tk_setPalette(background="#2E2E2E" if self.dark_theme else "#FFFFFF",
                                foreground="#FFFFFF" if self.dark_theme else "#000000")
        self.messenger_text.config(bg="#2E2E2E" if self.dark_theme else "white",
                                   fg="#FFFFFF" if self.dark_theme else "#000000")

    def send_command(self):
        command = self.input_var.get()
        if not command:
            return

        self.update_messenger(f"Вы: {command}", "user")
        self.input_var.set("")

        if command.startswith("/"):
            if command[1:] in self.commands:
                behavior = self.commands[command[1:]]["behavior"]
                if behavior == "text":
                    self.update_messenger(f"Бот: {self.commands[command[1:]]['response']}", "bot")
                elif behavior == "photo":
                    self.update_messenger(f"Бот: Отправлено фото", "bot")
                elif behavior == "keyboard":
                    self.update_messenger(f"Бот: Выберите действие", "bot")
            else:
                self.update_messenger(f"Бот: Неизвестная команда", "bot")

    def update_messenger(self, message, sender):
        self.messenger_text.config(state=tk.NORMAL)
        if sender == "user":
            self.messenger_text.insert(tk.END, f"Вы: {message}\n", "user")
        elif sender == "bot":
            self.messenger_text.insert(tk.END, f"Бот: {message}\n", "bot")
        elif sender == "system":
            self.messenger_text.insert(tk.END, f"Система: {message}\n", "system")
        self.messenger_text.config(state=tk.DISABLED)
        self.messenger_text.see(tk.END)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TelegramBotApp(root)
    root.mainloop()
