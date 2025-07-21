from interfaces import ParseManager, HistoryManager, ApiManager, ExecutorService

class Core:
    def __init__(self, parser: ParseManager, history: HistoryManager, api: ApiManager, executor: ExecutorService):
        self.parser = parser
        self.history = history
        self.api = api
        self.executor = executor

    def get_answer(self, question: str) -> str:
        try:
            # Отправка вопроса
            question_json = self.parser.text_to_json(question)
            history_json = self.history.get_history()
            messages = history_json + [question_json]
            response_json = self.api.send_query(messages)
            self.history.update_history(question_json)
            self.history.update_history(response_json)
            answer = self.parser.json_to_text(response_json)
            
            # Извлечение и исполнение bash
            bash_code = self.parser.extract_bash(answer)
            result = "Проанализируй результат выполнения:" + self.executor.execute_bash(bash_code)
            print(result)

            # Анализ результата исполнения 
            question_json = self.parser.text_to_json(result)
            messages += [question_json]
            response_json = self.api.send_query(messages)
            self.history.update_history(question_json)
            self.history.update_history(response_json)
            answer = self.parser.json_to_text(response_json)


            return answer
        except Exception as e:
            return f"Ошибка: {str(e)}"
