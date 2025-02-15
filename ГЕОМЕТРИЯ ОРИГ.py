import tkinter as tk
import math
import cmath

class GraphApp:
    def __init__(self, root, func_str):
        self.root = root
        self.root.title("График функции")

        # Область для отображения графика
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Настройки координатной сетки
        self.scale = 20  # Масштаб для отображения графика
        self.ox = 200    # Начало оси X (центр)
        self.oy = 200    # Начало оси Y (центр)

        # Рисуем оси координат
        self.draw_axes()

        # Построение графика
        self.plot_graph(func_str)

    def draw_axes(self):
        """Рисует оси координат и добавляет подписи."""
        # Ось X
        self.canvas.create_line(0, self.oy, 400, self.oy, fill="black", width=2)
        # Ось Y
        self.canvas.create_line(self.ox, 0, self.ox, 400, fill="black", width=2)

        # Подписи осей
        self.canvas.create_text(390, self.oy + 10, text="X", fill="black")
        self.canvas.create_text(self.ox + 10, 10, text="Y", fill="black")

        # Нанесение меток на оси
        for i in range(-10, 11):
            if i != 0:
                # Метки на оси X
                x = self.ox + i * self.scale
                self.canvas.create_line(x, self.oy - 5, x, self.oy + 5, fill="black")
                self.canvas.create_text(x, self.oy + 10, text=str(i), fill="black")

                # Метки на оси Y
                y = self.oy - i * self.scale
                self.canvas.create_line(self.ox - 5, y, self.ox + 5, y, fill="black")
                self.canvas.create_text(self.ox - 10, y, text=str(i), fill="black")

    def plot_graph(self, func_str):
        """Рисует график функции."""
        try:
            # Рисуем график
            previous_point = None
            for x in range(-self.ox, self.ox):
                try:
                    # Вычисляем значение y
                    x_val = x / self.scale
                    y_val = eval(func_str, {"x": x_val, "math": math})
                    y = self.oy - int(y_val * self.scale)

                    # Рисуем точку
                    self.canvas.create_oval(x + self.ox - 2, y - 2, x + self.ox + 2, y + 2, fill="blue", tags="graph")

                    # Соединяем точки линией
                    if previous_point:
                        self.canvas.create_line(previous_point[0], previous_point[1], x + self.ox, y, fill="blue", tags="graph")
                    previous_point = (x + self.ox, y)
                except:
                    # Пропускаем точки, где функция не определена
                    continue
        except Exception as e:
            tk.messagebox.showerror("Ошибка", f"Некорректная функция: {e}")

def график_функции(func_str):
    """Функция для создания окна с графиком."""
    root = tk.Tk()
    app = GraphApp(root, func_str)
    root.mainloop()

# Ввод функции через input()
if __name__ == "__main__":
    func_str = input("Введите функцию (например, x**2 или math.sin(x)): ")
    график_функции(func_str)
