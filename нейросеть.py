from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-ru-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

import torch

class NeuralNetwork:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.text_generator = pipeline("text-generation", model="gpt2", device=0 if self.device == "cuda" else -1)
        self.translator = pipeline("translation_ru_to_en", model="Helsinki-NLP/opus-mt-ru-en", device=0 if self.device == "cuda" else -1)
        self.qa_pipeline = pipeline("question-answering", device=0 if self.device == "cuda" else -1)

    def generate_text(self, prompt, max_length=50):
        """
        Генерация текста на основе заданного промта.
        """
        result = self.text_generator(prompt, max_length=max_length, num_return_sequences=1)
        return result[0]['generated_text']

    def translate_ru_to_en(self, text):
        """
        Перевод текста с русского на английский.
        """
        result = self.translator(text)
        return result[0]['translation_text']

    def answer_question(self, context, question):
        """
        Ответ на вопрос на основе заданного контекста.
        """
        result = self.qa_pipeline(question=question, context=context)
        return result['answer']

# Пример использования:
if __name__ == "__main__":
    nn = NeuralNetwork()

    # Генерация текста
    generated_text = nn.generate_text("Привет, как дела?")
    print("Сгенерированный текст:", generated_text)

    # Перевод текста
    translated_text = nn.translate_ru_to_en("Привет, как дела?")
    print("Переведенный текст:", translated_text)

    # Ответ на вопрос
    context = "Москва - столица России. Это крупнейший город страны, расположенный на реке Москва."
    question = "Какая река протекает в Москве?"
    answer = nn.answer_question(context, question)
    print("Ответ на вопрос:", answer)
