from interfaces import SettingsService
import os
import dotenv

class Settings(SettingsService):
    def get_settings(self):
        return {"api_key":os.getenv("API_KEY")}

    def change_settings(self, options):
        config = dotenv_values("../.env")
        with open('../.env', 'w') as f:
            for key, value in options.items():
                f.write(f"{key}={value}\n")

        load_dotenv()
        