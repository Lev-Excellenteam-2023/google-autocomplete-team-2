class TrieNode:
    def __init__(self):
        self.children = [None] * (26 + 10)  # for a-z 0-9
        self.positions = []
