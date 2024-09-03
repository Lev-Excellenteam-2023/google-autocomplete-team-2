import os
import time
from init_inverted_idx import build_inverted_index

file_name = 'archive.zip'

# Get the directory where the Python script is located
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Path to the zip file (assuming it's in the same directory as the script)
zip_file_path = os.path.join(main_project_dir, file_name)


def sentence_completion(zip_file_path):
    # Build the inverted index from the zip file
    inverted_index = build_inverted_index(zip_file_path)

    while True:
        # Get word from the user
        user_input = input("Enter a word to search (or type 'exit' to quit): ").strip().lower()

        if user_input == 'exit':
            print("Exiting...")
            break

        # Measure the time taken to search
        start_time = time.time()

        # Check if the word is in the inverted index
        if user_input in inverted_index:
            references = inverted_index[user_input]
            print(f"Found {len(references)} references for the word '{user_input}':")
            # for ref in references:
                # print(f"File: {ref[0]}, Line: {ref[1]}, Position: {ref[2]}")
        else:
            print(f"The word '{user_input}' was not found in the index.")

        end_time = time.time()
        search_time = end_time - start_time

        print(f"Search took {search_time:.4f} seconds\n")


if __name__ == "__main__":
    sentence_completion(zip_file_path)

