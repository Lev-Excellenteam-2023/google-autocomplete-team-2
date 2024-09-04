# import zipfile
# from collections import defaultdict
#
# def build_inverted_index(zip_file_path):
#     inverted_index = defaultdict(list)  # Using defaultdict to handle missing keys easily
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
#         # Iterate through each file in the zip
#         for file_name in zip_file.namelist():
#             if file_name.endswith('.txt'):  # Process only .txt files
#                 with zip_file.open(file_name) as file:
#                     for line_number, line in enumerate(file, start=1):
#                         # Tokenize the line into words
#                         words = line.decode('utf-8').strip().split()
#                         for word in words:
#                             # Store file name and line number for each word
#                             inverted_index[word].append((file_name, line_number))
#     return inverted_index
#
# def search_inverted_index(inverted_index, search_term):
#     # Look up the search term in the index
#     results = inverted_index.get(search_term, [])
#     if results:
#         print(f"Found '{search_term}' in the following files/lines:")
#         for file_name, line_number in results:
#             print(f"- {file_name}, Line {line_number}")
#     else:
#         print(f"'{search_term}' not found in any file.")
# # Example usage:
# zip_file_path = 'your_archive.zip'
# index = build_inverted_index(zip_file_path)
# search_term = input("Enter the search term: ")
# search_inverted_index(index, search_term)


import zipfile
import os
import re
from collections import defaultdict
import cProfile
file_name = 'archive.zip'

# Get the directory where the Python script is located
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Path to the zip file (assuming it's in the same directory as the script)
zip_file_path_1 = os.path.join(main_project_dir, file_name)


# # Open the zip file
# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     # Iterate over each file in the zip
#     for file_name in zip_ref.namelist():
#         # Check if the file is a text file
#         if file_name.endswith('.txt'):
# Open and read the text file
# with zip_ref.open(file_name) as file:
#     content = file.read().decode('utf-8')
#     print(f"Content of {file_name}:")
#     print(content)
#     print("-" * 40)  # Just a separator between files


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


def search_consecutive_words(inverted_index, words):
    # Convert the search words to lowercase (to match the indexing)
    words = [word.lower() for word in words]

    # Start with the positions of the first word
    if words[0] not in inverted_index:
        return []

    result_positions = inverted_index[words[0]]

    for i in range(1, len(words)):
        word_positions = inverted_index.get(words[i], [])
        next_result_positions = []

        # Check each position in result_positions to see if the next word is consecutive
        for file_name_1, line_number, position in result_positions:
            # Find the corresponding next word position in the same file and line
            if (file_name_1, line_number, position + 1) in word_positions:
                next_result_positions.append((file_name_1, line_number, position + 1))

        # Update the positions to the new filtered list
        result_positions = next_result_positions

    # Convert the result back to the format showing the start of the word sequence
    final_results = [(file_name_1, line_number, position - len(words) + 1) for (file_name_1, line_number, position) in
                     result_positions]

    return final_results


inverted = build_inverted_index(zip_file_path_1)
# print(inverted.get('all'))

sen = "all"
search_words = sen.split(" ")
print(search_words)
matches = search_consecutive_words(inverted, search_words)
print(len(matches))
cProfile.run('main()')

# # print files structure:
# import os
#
# file_name = 'archive.zip'
#
# # Get the directory where the Python script is located
# main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # not so good..
# # current_dir = os.path.dirname(os.path.abspath(__file__))
# # print(current_dir)
# # print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
# # Path to the zip file (assuming it's in the same directory as the script)
# zip_file_path = os.path.join(main_project_dir, file_name)
#
# def print_tree_structure(file_list):
#     tree = {}
#
#     for file in file_list:
#         parts = file.split('/')
#         current_level = tree
#         for part in parts:
#             if part not in current_level:
#                 current_level[part] = {}
#             current_level = current_level[part]
#
#     def print_tree(level, indent=""):
#         for i, (key, subtree) in enumerate(sorted(level.items())):
#             is_last = i == len(level) - 1
#             print(f"{indent}{'└── ' if is_last else '├── '}{key}")
#             if isinstance(subtree, dict):
#                 print_tree(subtree, indent + ("    " if is_last else "│   "))
#
#     print_tree(tree)
#
# # Open the zip file
# with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#     # Get the list of all files and directories
#     all_files_dirs = zip_ref.namelist()
#
#     # Print the tree structure
#     print(f"{os.path.basename(zip_file_path)}")
#     print_tree_structure(all_files_dirs)
