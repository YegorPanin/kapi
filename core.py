from interfaces import IParser, IHistory, IApi
import time

class Core:
    def __init__(self, parser: IParser, history: IHistory, api: IApi):
        self.parser = parser
        self.history = history
        self.api = api

    def get_answer(self, question: str) -> str:
        try:
            question_json = self.parser.text_to_json(question)
            history_json = self.history.get_history()
            # Добавляем системный промт в начало массива сообщений
            system_prompt = {
                "role": "system",
                "content": "Ты дружелюбный и полезный Линукс ИИ-помощник Kapi, отвечающий на русском языке с позитивным тоном и эмодзи 😊. Стремись давать краткие, но содержательные ответы."
            }
            full_messages = [system_prompt] + history_json + [question_json]
            data = {
                "model": "lgai/exaone-3-5-32b-instruct",
                "messages": full_messages
            }
            response_json = self.api.send_query(data)
            self.history.update_history(question_json)
            self.history.update_history(response_json)
            answer = self.parser.json_to_text(response_json)
            return answer
        except Exception as e:
            if "Error code: 429" in str(e):
                print("Превышен лимит запросов, ждем 200 секунд...")
                time.sleep(200)
                return self.get_answer(question)  # Повторяем запрос
            return f"Ошибка: {str(e)}"