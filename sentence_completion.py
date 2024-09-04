import os
import re
import time

from build_dict_database import build_dict

file_name = 'archive.zip'

# Get the directory where the Python script is located
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Path to the zip file (assuming it's in the same directory as the script)
file_path = os.path.join(main_project_dir, file_name)


def sentence_completion(zip_file_path):
    # try:
    #     inverted_index = build_inverted_index_trie(zip_file_path)
    #     if inverted_index is None:
    #         print("Failed to build the inverted index. Exiting...")
    #         return
    # except Exception as e:
    #     print(e)
    #     return

    try:
        dict_database = build_dict(zip_file_path)
        if dict is None:
            print("Failed to build the inverted index. Exiting...")
            return
    except Exception as e:
        print(e)
        return

    while True:
        # Get sub sentence from the user
        search_query = get_user_input()

        if search_query == 'exit':
            print("Exiting...")
            break

        # Measure the time taken to search
        start_time = time.time()  # TODO: del

        found_any = False
        found = 0

        for key in dict_database:
            if search_query in key:
                found += 1
                references = dict_database[key]
                found_any = True
                # print(f"Found {len(references)} references for the phrase '{search_query}' in '{key}':")
                # for ref in references:
                #     print(f"File: {ref.file_name}, Line: {ref.line_number}, Full sentence: {ref.full_sentence}")
        if not found_any:
            print(f"The phrase '{search_query}' was not found in the index.")

        print(f"found - {found} results.")

        end_time = time.time()  # TODO: del
        search_time = end_time - start_time  # TODO: del
        print(f"Search took {search_time:.4f} seconds\n")  # TODO: del


def get_user_input():
    user_input = input("Enter a word to search (or type 'exit' to quit): ").strip().lower()
    cleaned_input = re.sub(r'[^a-z0-9\s]', '', user_input)
    words = re.findall(r'[a-z0-9]+', cleaned_input)
    print(words)
    return ' '.join(words)


# def sentence_completion_first_try(zip_file_path):
#     # Build the inverted index from the zip file
#     inverted_index = build_inverted_index(zip_file_path)
#
#     while True:
#         # Get word from the user
#         user_input = input("Enter a word to search (or type 'exit' to quit): ").strip().lower()
#
#         if user_input == 'exit':
#             print("Exiting...")
#             break
#
#         # Measure the time taken to search
#         start_time = time.time()
#
#         # Check if the word is in the inverted index
#         if user_input in inverted_index:
#             references = inverted_index[user_input]
#             print(f"Found {len(references)} references for the word '{user_input}':")
#             # for ref in references:
#                 # print(f"File: {ref[0]}, Line: {ref[1]}, Position: {ref[2]}")
#         else:
#             print(f"The word '{user_input}' was not found in the index.")
#
#         end_time = time.time()
#         search_time = end_time - start_time
#
#         print(f"Search took {search_time:.4f} seconds\n")


if __name__ == "__main__":
    sentence_completion(file_path)
