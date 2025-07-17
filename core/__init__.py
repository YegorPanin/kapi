from interfaces import ParseManager, HistoryManager, ApiManager

class Core:
    def __init__(self, parser: ParseManager, history: HistoryManager, api: ApiManager):
        self.parser = parser
        self.history = history
        self.api = api

    def get_answer(self, question: str) -> str:
        try:
            question_json = self.parser.text_to_json(question)
            history_json = self.history.get_history()
            messages = history_json + [question_json]
            response_json = self.api.send_query(messages)
            self.history.update_history(question_json)
            self.history.update_history(response_json)
            answer = self.parser.json_to_text(response_json)
            return answer
        except Exception as e:
            return f"Ошибка: {str(e)}"