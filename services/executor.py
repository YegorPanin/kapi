from abc import ABC, abstractmethod
from interfaces import ExecutorService
import subprocess


class BashExecutor(ExecutorService):
    def execute_bash(self, script: str) -> str:
        try:
            # Выполняем скрипт в bash-оболочке
            result = subprocess.run(
                ["bash", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            output = result.stdout
            return output

        except subprocess.CalledProcessError as e:
            # Если скрипт завершился с ненулевым кодом, возвращаем stderr
            error_output = e.stderr.strip()
            print(f"Ошибка при выполнении скрипта:\n{error_output}")
            return error_output
