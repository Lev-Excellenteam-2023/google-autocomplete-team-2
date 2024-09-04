class Position:
    def __init__(self, file_name, line_number, char_position):
        self.file_name = file_name
        self.line_number = line_number
        self.char_position = char_position
        # self.word_position = word_position

    def __repr__(self):
        return f"File: {self.file_name}, Line: {self.line_number}, Char Pos: {self.char_position}"
        # return f"File: {self.file_name}, Line: {self.line_number}, Word Pos: {self.word_position}, Char Pos: {
        # self.char_position}"
