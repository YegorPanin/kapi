import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PySide6.QtCore import Qt
from core import Core
from services.parser import Parser
from services.database import JsonHistory
from services.api import TogetherApi

# Загрузка переменных окружения
load_dotenv()

class ChatApp(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setWindowTitle("Kapi - Чат-бот")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Область вывода диалога
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        # Поле ввода
        input_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Введите ваш вопрос...")

        # Кнопка отправки
        send_button = QPushButton("Отправить")
        send_button.clicked.connect(self.handle_send)

        input_layout.addWidget(self.input_line)
        input_layout.addWidget(send_button)

        layout.addWidget(self.chat_area)
        layout.addLayout(input_layout)

        self.setLayout(layout)

        # Обработка Enter
        self.input_line.returnPressed.connect(self.handle_send)

    def handle_send(self):
        question = self.input_line.text()
        if question.strip() == "":
            return

        self.chat_area.append(f"Вы: {question}")
        self.input_line.clear()

        try:
            answer = self.core.get_answer(question)
            self.chat_area.append(f"Kapi: {answer}")
        except Exception as e:
            self.chat_area.append(f"Kapi: Ошибка: {str(e)}")

    def closeEvent(self, event):
        """Очистка истории при закрытии окна"""
        self.core.history.delete_history()
        print("История очищена.")
        event.accept()


def main():
    # Инициализация приложения
    app = QApplication([])

    # Инициализация компонентов
    parser = Parser()
    history = JsonHistory(file_path="resources/history.json")
    api = TogetherApi()
    core = Core(parser, history, api)

    # Запуск GUI
    window = ChatApp(core)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()