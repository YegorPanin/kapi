from interfaces import IParser, IHistory, IApi

class Core:
    def __init__(self, parser: IParser, history: IHistory, api: IApi):
        self.parser = parser
        self.history = history
        self.api = api

    def get_answer(self, question: str) -> str:
        try:
            # 1. Преобразуем вопрос в JSON
            question_json = self.parser.text_to_json(question)

            # 2. Получаем историю
            history_json = self.history.get_history()

            # 3. Отправляем запрос
            response_json = self.api.send_query({
                "question": question_json,
                "history": history_json
            })

            # 4. Обновляем историю
            self.history.update_history(response_json)

            # 5. Преобразуем ответ в текст
            answer = self.parser.json_to_text(response_json)

            return answer

        except Exception as e:
            return f"Ошибка: {str(e)}"