from interfaces import ParseManager
import re

class Parser(ParseManager):
    def text_to_json(self, text: str) -> dict:
        return {
            "role": "user",
            "content": text
        }

    def json_to_text(self, json: dict) -> str:
        content = json['content']
        cleaned_content = re.sub(r'<think>.*</think>', '', content, flags=re.DOTALL).strip()
        return cleaned_content