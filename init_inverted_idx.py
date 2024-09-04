import zipfile
from collections import defaultdict
import re


def build_inverted_index(zip_file_path):
    inverted_index = defaultdict(list)
    # Open the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Iterate over each file in the zip
        for file_name_0 in zip_ref.namelist():
            # Only process text files
            if file_name_0.endswith('.txt'):
                with zip_ref.open(file_name_0) as file:
                    content = file.read().decode('utf-8').splitlines()

                    # Process each line in the file
                    for line_number, line in enumerate(content):
                        # Tokenize the line into words
                        words = re.findall(r'\b\w+\b', line.lower())

                        # Add each word to the inverted index with the file name and position
                        for position, word in enumerate(words):
                            inverted_index[word].append((file_name_0, line_number, position))

    return inverted_index
