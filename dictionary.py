import re
import time
import zipfile
from collections import defaultdict
from autocomplete_data import AutoCompleteData
from position import Position
from search import is_partial_match, calculate_score


class Dictionary:
    def __init__(self, k=5):
        self.max_results = k
        self.data_dict = defaultdict(list)

    def build_dict(self, zip_file_path):
        print("Building dictionary...")  # TODO: del
        start_time = time.time()  # TODO: del

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.endswith('.txt'):
                        with zip_ref.open(file_name) as file:
                            for line_number, line in enumerate(file, 1):
                                line = line.decode('utf-8').strip()
                                normalized_line = self.normalize_line(line)
                                if normalized_line:
                                    self.data_dict[normalized_line].append(Position(line, file_name, line_number))

            end_time = time.time()  # TODO: del
            print(f"Building dictionary took {end_time - start_time:.4f} seconds")  # TODO: del

        except zipfile.BadZipFile:
            raise zipfile.BadZipFile(f"The file '{zip_file_path}' is not a valid ZIP file.")
        except Exception as e:
            raise Exception(f"An error occurred while processing the file '{zip_file_path}': {str(e)}")

    @staticmethod
    def normalize_line(line):
        return ' '.join(re.findall(r'[a-zA-Z0-9]+', line.lower()))

    def get_best_k_completions(self, user_input):
        matches = self._perfect_matches(user_input)

        if len(matches) < self.max_results:
            # search for partial matches
            matches += self._partial_match(user_input)

        matches.sort(key=lambda x: x.completed_sentence)
        print(f"found - {len(matches)} results.")  # TODO: del

        # return matches
        return matches[:self.max_results]

    def _perfect_matches(self, user_input):
        perfect_matches = []
        for key in self.data_dict:
            if user_input in key:
                positions = self.data_dict[key]
                for pos in positions:
                    perfect_matches.append(AutoCompleteData(pos.full_sentence, pos.file_name,
                                                            pos.line_number, 2 * len(user_input)))
        return perfect_matches

    def _partial_match(self, user_input):
        partial_matches = []
        for key in self.data_dict:
            result = is_partial_match(user_input, key)
            if result:
                positions = self.data_dict[key]
                for pos in positions:
                    partial_matches.append(AutoCompleteData(pos.full_sentence, pos.file_name,
                                                            pos.line_number, calculate_score(user_input, result)))
        return partial_matches
