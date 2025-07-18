import os
from dotenv import load_dotenv
from core import Core
from services.parser import Parser
from services.database import JsonHistory
from services.api import TogetherApi

settings = load_dotenv()

def main():
    parser = Parser()
    history = JsonHistory(file_path="resources/history.json")
    api = TogetherApi()
    core = Core(parser, history, api)
    try:    
        while True:
            question = input("You: ")
            if question.lower() == "exit":
                break
            answer = core.get_answer(question)
            print(f"Kapi: {answer}\n")
    finally:
        history.delete_history()
        print("История очищена.")

if __name__ == "__main__":
    main()