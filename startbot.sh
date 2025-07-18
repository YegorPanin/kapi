#!/bin/bash

VENV_NAME=".venv"

# Проверка наличия виртуальной среды
if [ ! -d "$VENV_NAME" ]; then
    echo "Виртуальная среда не найдена. Создаю $VENV_NAME..."
    python3 -m venv "$VENV_NAME"
else
    echo "Виртуальная среда уже существует."
fi

# Активация виртуальной среды
source "$VENV_NAME/bin/activate"

# Проверка наличия requirements.txt и установка зависимостей
if [ -f "requirements.txt" ]; then
    echo "Найден requirements.txt. Устанавливаю зависимости..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "Файл requirements.txt не найден. Пропускаю установку зависимостей."
    exit
fi

echo "Настройка завершена."
echo "Запускаем сервис..."
python3 main.py