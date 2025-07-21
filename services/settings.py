from interfaces import SettingsService
import os
from dotenv import dotenv_values, load_dotenv

class Settings(SettingsService):
    def get_settings(self):
        return {
            "api_key": os.getenv("API_KEY"),
            "model": os.getenv("MODEL", "lgai/exaone-3-5-32b-instruct"),
            "system_prompt": os.getenv("SYSTEM_PROMPT", "Ты дружелюбный и полезный Линукс ИИ-помощник Kapi, отвечающий на русском языке с позитивным тоном и эмодзи 😊 но не используй эмодзи слишком много. Стремись давать краткие, но содержательные ответы.")
        }

    def change_settings(self, options):
        config = dotenv_values("../.env")
        config.update(options)
        with open('../.env', 'w') as f:
            for key, value in config.items():
                f.write(f"{key}={value}\n")
        load_dotenv()