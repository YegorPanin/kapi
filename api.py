from together import Together
from interfaces import IApi

class TogetherApi(IApi):
    def __init__(self, api_key):
        self.client = Together(api_key=api_key)

    def send_query(self, data: dict) -> dict:
        response = self.client.chat.completions.create(**data)
        return response.choices[0].message.dict()