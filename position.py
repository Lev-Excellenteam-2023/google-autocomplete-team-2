class Position:
    def __init__(self, full_sentence, file_name, line_number):
        self.full_sentence = full_sentence
        self.file_name = file_name
        self.line_number = line_number

    def __str__(self):
        return f"Full sentence: {self.full_sentence}, File: {self.file_name}, Line: {self.line_number}"
