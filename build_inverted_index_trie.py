import re
import time
import zipfile

from inverted_index_trie import InvertedIndexTrie
from position import Position


def build_inverted_index_trie(zip_file_path):
    trie = InvertedIndexTrie()

    print("Build starting now")  # TODO: del
    start_time = time.time()  # TODO: del

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.txt'):
                    with zip_ref.open(file_name) as file:
                        content = file.read().decode('utf-8').splitlines()

                        for line_number, line in enumerate(content):
                            words = re.findall(r'[a-zA-Z0-9]+', line.lower())
                            char_position = 0

                            for word in words:
                                # insert this word and all his sub words
                                insert_word_to_trie(trie, word, file_name, line_number, char_position)
                                # insert only this word
                                # trie.insert(word, Position(file_name, line_number, char_position))
                                char_position += len(word)  # TODO: maby  +1 for space between words

        end_time = time.time()  # TODO: del
        search_time = end_time - start_time  # TODO: del
        print(f"Building took {search_time:.4f} seconds\n")  # TODO: del

    except zipfile.BadZipFile:
        raise zipfile.BadZipFile(f"The file '{zip_file_path}' is not a valid ZIP file.")

    except Exception as e:
        raise Exception(f"An error occurred while processing the file '{zip_file_path}': {str(e)}")

    return trie


def insert_word_to_trie(trie, word, file_name, line_number, char_position):
    for start in range(len(word)):
        for end in range(start + 1, len(word) + 1):
            trie.insert(word[start:end], Position(file_name, line_number, char_position + start))
            # TODO: maby not build Position, only send the data
