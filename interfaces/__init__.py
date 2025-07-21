from abc import ABC, abstractmethod

class ParseManager(ABC):
    @abstractmethod
    def text_to_json(self, text: str) -> dict:
        pass

    @abstractmethod
    def json_to_text(self, data: dict) -> str:
        pass

    @abstractmethod
    def extract_bash(self, text: str) -> str:
        pass

class HistoryManager(ABC):
    @abstractmethod
    def get_history(self) -> list:
        pass

    @abstractmethod
    def update_history(self, note: dict) -> None:
        pass

    @abstractmethod
    def delete_history(self) -> None:
        pass

class ApiManager(ABC):
    @abstractmethod
    def send_query(self, data: dict) -> dict:
        pass

class SettingsService(ABC):
    @abstractmethod
    def change_settings(self, options: dict) -> None:
        pass
    
    @abstractmethod
    def get_settings() -> dict:
        pass

class ExecutorService(ABC):
    @abstractmethod
    def execute_bash(self, script: str) -> str:
        pass