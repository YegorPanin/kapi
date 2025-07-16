class Parser:
    def question_to_json(self, question) -> dict:
        json = {
            "role": "user",
            "content": question
        }
        return json
    
    def json_to_text(self, json: dict) -> str:
        return json['content']