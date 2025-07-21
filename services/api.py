import os
import time
from together import Together
from interfaces import ApiManager

class TogetherApi(ApiManager):
    DEFAULT_MODEL = "lgai/exaone-3-5-32b-instruct"
    SYSTEM_PROMPT = {
        "role": "system",
        "content": '''
        Ты дружелюбный и полезный Линукс ИИ-помощник Kapi.
        Твоя задача - генерировать однострочные bash-команды в зависимости от желания пользователя. 
        Скрипты для исполнения записывай в конце ответа СТРОГО в виде одной строки вида ```bash```. ВАЖНО: ГЕНЕРИРУЙ ТОЛЬКО ОДНОСТРОЧНЫЕ команды. Как пользователь
        '''
    }

    def __init__(self):
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable is not set.")
        self.client = Together(api_key=api_key)

    def send_query(self, messages: list, model: str = None) -> dict:
        if model is None:
            model = self.DEFAULT_MODEL
        full_messages = [self.SYSTEM_PROMPT] + messages
        data = {
            "model": model,
            "messages": full_messages
        }
        while True:
            try:
                response = self.client.chat.completions.create(**data)
                return response.choices[0].message.dict()
            except Exception as e:
                if "Error code: 429" in str(e):
                    print("Превышен лимит запросов, ждем 200 секунд...")
                    time.sleep(200)
                else:
                    raise e