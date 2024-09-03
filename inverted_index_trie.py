from position import Position
from trie_node import TrieNode


class InvertedIndexTrie:
    def __init__(self):
        self.root = TrieNode()

    @staticmethod
    def _char_to_index(char):
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        elif char.isdigit():
            return ord(char) - ord('0') + 26
        return None

    def insert(self, word, position):
        node = self.root
        for i, char in enumerate(word):
            index = self._char_to_index(char)
            if index is not None:
                if node.children[index] is None:
                    node.children[index] = TrieNode()
                node = node.children[index]
                node.positions.append(Position(position.file_name, position.line_number, position.char_position + i))

    def search(self, prefix):
        node = self.root
        for char in prefix:
            index = self._char_to_index(char)
            if index is None or node.children[index] is None:
                return []
            node = node.children[index]
        return node

    def search_and_retrieve(self, word):
        node = self.search(word)
        if node is not None and node.positions:
            return True, node.positions
        return False, []

    def __contains__(self, word):  # overloading to use 'in' (if word in InvertedIndexTrie:)
        node = self.search(word)
        return node is not None and bool(node.positions)

    def __getitem__(self, word):  # overloading to use index (InvertedIndexTrie[index])
        node = self.search(word)
        if node is None:
            raise KeyError(f"'{word}' not found in the Trie")
        return node.positions
