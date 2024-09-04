class AutoCompleteData:
    def __init__(self, completed_sentence: str, source: str, line_number: int, score: int):
        self.completed_sentence = completed_sentence
        self.source = source
        self.line_number = line_number
        self.score = score

    def __str__(self):
        return f"{self.completed_sentence} ({self.source} {self.line_number}), {self.score}"
