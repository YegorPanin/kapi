from abc import ABC, abstractmethod

class IParser(ABC):
    @abstractmethod
    def text_to_json(self, text: str) -> dict:
        pass

    @abstractmethod
    def json_to_text(self, data: dict) -> str:
        pass

class IHistory(ABC):
    @abstractmethod
    def get_history(self) -> list:
        pass

    @abstractmethod
    def update_history(self, note: dict) -> None:
        pass

    @abstractmethod
    def delete_history(self) -> None:
        pass

class IApi(ABC):
    @abstractmethod
    def send_query(self, data: dict) -> dict:
        pass