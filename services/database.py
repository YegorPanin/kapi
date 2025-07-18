import json
from interfaces import HistoryManager

class JsonHistory(HistoryManager):
    def __init__(self, file_path="resources/history.json"):
        self.file_path = file_path
        try:
            with open(self.file_path, "r") as f:
                content = f.read()
                self.history = json.loads(content) if content.strip() else []
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            with open(self.file_path, "w") as f:
                json.dump(self.history, f)

    def get_history(self) -> list:
        return self.history

    def update_history(self, note: dict) -> None:
        self.history.append(note)
        with open(self.file_path, "w") as f:
            json.dump(self.history, f)

    def delete_history(self) -> None:
        self.history = []
        with open(self.file_path, "w") as f:
            json.dump(self.history, f)