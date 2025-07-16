class FileMaster:
    def get_json_file(self):
        content = json.load(".history.json")
        return content
