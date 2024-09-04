import os
import time
import cProfile

from dictionary import Dictionary

file_name = 'archive.zip'
# Get the directory where the Python script is located
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# Path to the zip file (assuming it's in the same directory as the script)
file_path = os.path.join(main_project_dir, file_name)


def sentence_completion(zip_file_path):
    try:
        dict_database = Dictionary()
        dict_database.build_dict(zip_file_path)
        if dict_database is None:
            print("Failed to build the inverted index. Exiting...")
            return
    except Exception as e:
        print(e)
        return

    while True:
        # Get sub sentence from the user
        original_inp, search_query = get_user_input()

        if search_query == 'exit':
            print("Exiting...")
            break

        # Measure the time taken to search
        start_time = time.time()  # TODO: del

        matches = dict_database.get_best_k_completions(search_query)

        for i, m in enumerate(matches, 1):
            print(f"{i}. {m}")

        # print(f"found - {len(matches)} results.")  # TODO: del
        end_time = time.time()  # TODO: del
        search_time = end_time - start_time  # TODO: del
        print(f"Search took {search_time:.4f} seconds\n")  # TODO: del


def get_user_input():
    user_input = input("Enter a word to search (or type 'exit' to quit): ").strip().lower()
    return user_input, Dictionary.normalize_line(user_input)


if __name__ == "__main__":
    sentence_completion(file_path)
    # cProfile.run('sentence_completion(file_path)')

