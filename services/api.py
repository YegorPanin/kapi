import os
import time
from together import Together
from interfaces import ApiManager

class TogetherApi(ApiManager):
    def __init__(self):
        self.model = os.getenv("MODEL", "lgai/exaone-3-5-32b-instruct")
        self.system_prompt = {
            "role": "system",
            "content": os.getenv("SYSTEM_PROMPT", "Ты дружелюбный и полезный Линукс ИИ-помощник Kapi, отвечающий на русском языке с позитивным тоном и эмодзи 😊 но не используй эмодзи слишком много. Стремись давать краткие, но содержательные ответы.")
        }
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable is not set.")
        self.client = Together(api_key=api_key)

    def send_query(self, messages: list, model: str = None) -> dict:
        if model is None:
            model = self.model
        full_messages = [self.system_prompt] + messages
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