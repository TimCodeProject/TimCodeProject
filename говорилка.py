import pyttsx3

class ГолосовойАссистент:
    def __init__(self):
        self.двигатель = pyttsx3.init()
        self.голоса = self.двигатель.getProperty('voices')
        self.установить_голос(0)  # По умолчанию мужской голос

    def установить_голос(self, индекс):
        """Устанавливает голос по индексу (0 - мужской, 1 - женский)"""
        if 0 <= индекс < len(self.голоса):
            self.двигатель.setProperty('voice', self.голоса[индекс].id)
        else:
            print("Ошибка: неверный индекс голоса")

    def сказать(self, текст):
        """Произносит переданный текст"""
        self.двигатель.say(текст)
        self.двигатель.runAndWait()

    def установить_скорость(self, скорость):
        """Устанавливает скорость речи"""
        self.двигатель.setProperty('rate', скорость)

    def установить_громкость(self, громкость):
        """Устанавливает громкость (от 0.0 до 1.0)"""
        if 0.0 <= громкость <= 1.0:
            self.двигатель.setProperty('volume', громкость)
        else:
            print("Ошибка: громкость должна быть от 0.0 до 1.0")

    def остановить(self):
        """Останавливает текущее воспроизведение"""
        self.двигатель.stop()

    def сохранить_в_аудиофайл(self, текст, имя_файла):
        """Сохраняет произнесенный текст в аудиофайл"""
        self.двигатель.save_to_file(текст, имя_файла)
        self.двигатель.runAndWait()

# Пример использования
if __name__ == "__main__":
    ассистент = ГолосовойАссистент()
    ассистент.сказать("Привет, как дела?")
    ассистент.установить_скорость(350)
    ассистент.установить_громкость(0.8)
    ассистент.сказать("Это тест скорости и громкости.")
    ассистент.сохранить_в_аудиофайл("Этот текст будет сохранен в файл.", "тест.mp3")
