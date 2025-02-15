import tkinter as tk
import math

class GraphCanvas(tk.Canvas):
    def __init__(self, master, width=400, height=400, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.scale = 40  # Масштаб графика (1 единица = 40 пикселей)
        self.origin_x = self.width // 2
        self.origin_y = self.height // 2

    def draw_axes(self):
        # Оси координат
        self.create_line(0, self.origin_y, self.width, self.origin_y, fill="black")  # Ось X
        self.create_line(self.origin_x, 0, self.origin_x, self.height, fill="black")  # Ось Y

        # Разметка и подписи на оси X
        for x in range(-self.origin_x, self.origin_x + 1, self.scale):
            screen_x = x + self.origin_x
            self.create_line(screen_x, self.origin_y - 5, screen_x, self.origin_y + 5, fill="black")  # Деления
            if x != 0:  # Подписи (кроме 0 на пересечении осей)
                label = str(x // self.scale)
                self.create_text(screen_x, self.origin_y + 10, text=label, fill="black")

        # Разметка и подписи на оси Y
        for y in range(-self.origin_y, self.origin_y + 1, self.scale):
            screen_y = y + self.origin_y
            self.create_line(self.origin_x - 5, screen_y, self.origin_x + 5, screen_y, fill="black")  # Деления
            if y != 0:  # Подписи (кроме 0 на пересечении осей)
                label = str(-y // self.scale)
                self.create_text(self.origin_x + 10, screen_y, text=label, fill="black")

    def draw_grid(self):
        # Сетка (клеточный фон)
        for x in range(-self.origin_x, self.origin_x + 1, self.scale):
            screen_x = x + self.origin_x
            self.create_line(screen_x, 0, screen_x, self.height, fill="lightgray")  # Вертикальные линии

        for y in range(-self.origin_y, self.origin_y + 1, self.scale):
            screen_y = y + self.origin_y
            self.create_line(0, screen_y, self.width, screen_y, fill="lightgray")  # Горизонтальные линии

    def plot_function(self, func_str):
        self.draw_grid()  # Сначала рисуем сетку
        self.draw_axes()  # Затем оси координат
        step = 0.003  # Уменьшаем шаг для увеличения точности
        for i in range(int(-self.origin_x / step), int(self.origin_x / step)):
            try:
                x = i * step
                # Преобразуем строку в функцию
                y = eval(func_str, {"math": math, "x": x})
                # Преобразуем x и y в координаты экрана
                screen_x = x * self.scale + self.origin_x
                screen_y = -y * self.scale + self.origin_y
                self.create_rectangle(screen_x, screen_y, screen_x + 1, screen_y + 1, outline="blue")
            except:
                pass

def график_функции(функция_строка):
    # Создаем окно
    root = tk.Tk()
    root.title("График функции")

    # Создаем canvas для рисования
    canvas = GraphCanvas(root)
    canvas.pack()

    # Рисуем график
    canvas.plot_function(функция_строка)

    # Запускаем главный цикл
    root.mainloop()
