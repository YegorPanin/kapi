from core import Core
from parser import Parser
from database import JsonHistory
from api import TogetherApi

API_KEY = "API"

def main():
    parser = Parser()
    history = JsonHistory(file_path="history.json")
    api = TogetherApi(api_key=API_KEY)
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