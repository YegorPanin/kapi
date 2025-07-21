from interfaces import SettingsService
from pathlib import Path
import os
from dotenv import dotenv_values, load_dotenv

class Settings(SettingsService):
    def get_settings(self):
        return {"API_KEY": os.getenv("API_KEY")}

    def change_settings(self, options: dict) -> None:
        env_path = Path(__file__).parent.parent / ".env"  # Путь относительно файла
        print(f"Используемый .env: {env_path.resolve()}")

        # Создать файл, если не существует
        env_path.touch(exist_ok=True)

        # Чтение текущих данных
        if env_path.exists():
            current_config = dotenv_values(env_path)
        else:
            current_config = {}

        # Обновление параметров
        for key, value in options.items():
            current_config[key] = value

        # Запись обновленного файла
        try:
            with env_path.open("w") as f:
                for key, value in current_config.items():
                    f.write(f"{key}={value}\n")
            load_dotenv(env_path, override=True)
            print("Настройки успешно обновлены.")
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")