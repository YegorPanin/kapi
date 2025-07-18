import os
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QDialog, QFormLayout, QComboBox, QMessageBox
from PySide6.QtCore import Qt
from core import Core
from services.parser import Parser
from services.database import JsonHistory
from services.api import TogetherApi
from services.settings import Settings
from interfaces import SettingsService

# Загрузка переменных окружения
load_dotenv()

class SettingsWindow(QDialog):
    def __init__(self, settings_service, parent=None):
        super().__init__(parent)
        self.settings_service = settings_service
        self.setWindowTitle("Настройки")
        self.layout = QFormLayout(self)

        self.settings_fields = {}

        # Получаем текущие настройки
        self.current_settings = self.settings_service.get_settings()

        # Создаём поля ввода для каждой настройки
        for key, value in self.current_settings.items():
            if isinstance(value, str):
                line_edit = QLineEdit(value)
                self.layout.addRow(QLabel(key), line_edit)
                self.settings_fields[key] = line_edit
            elif isinstance(value, bool):
                combo = QComboBox()
                combo.addItems(["True", "False"])
                combo.setCurrentText(str(value))
                self.layout.addRow(QLabel(key), combo)
                self.settings_fields[key] = combo
            else:
                line_edit = QLineEdit(str(value))
                self.layout.addRow(QLabel(key), line_edit)
                self.settings_fields[key] = line_edit

        # Кнопки
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

    def save_settings(self):
        updated_settings = {}
        for key, widget in self.settings_fields.items():
            if isinstance(widget, QLineEdit):
                val = widget.text()
                # Попытка привести к типу оригинального значения
                orig_val = self.current_settings[key]
                if isinstance(orig_val, bool):
                    updated_settings[key] = val.lower() in ('true', '1', 't', 'y', 'yes')
                elif isinstance(orig_val, int):
                    updated_settings[key] = int(val)
                elif isinstance(orig_val, float):
                    updated_settings[key] = float(val)
                else:
                    updated_settings[key] = val
            elif isinstance(widget, QComboBox):
                updated_settings[key] = widget.currentText() == "True"

        try:
            self.settings_service.change_settings(updated_settings)
            QMessageBox.information(self, "Настройки", "Настройки успешно сохранены.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки: {e}")


class ChatApp(QWidget):
    def __init__(self, core, settings_service):
        super().__init__()
        self.core = core
        self.settings_service = settings_service
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

        # Строка с кнопкой настроек
        settings_layout = QHBoxLayout()
        settings_button = QPushButton("...")
        settings_button.setFixedWidth(30)
        settings_button.clicked.connect(self.open_settings)
        settings_layout.addStretch()
        settings_layout.addWidget(settings_button)

        layout.addWidget(self.chat_area)
        layout.addLayout(input_layout)
        layout.addLayout(settings_layout)

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

    def open_settings(self):
        dialog = SettingsWindow(self.settings_service, self)
        dialog.exec()

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

    # Инициализация сервиса настроек
    settings_service = Settings()

    # Запуск GUI
    window = ChatApp(core, settings_service)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()