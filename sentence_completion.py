import os
import time
import cProfile
from dictionary import Dictionary

file_name = 'archive.zip'
# file_name = 'aa.zip'
# Get the directory where the Python script is located
main_project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# Path to the zip file (assuming it's in the same directory as the script)
file_path = os.path.join(main_project_dir, file_name)


def sentence_completion(zip_file_path):
    print("Loading the files and preparing the system...")
    try:
        dict_database = Dictionary()
        dict_database.build_dict(zip_file_path)
        if dict_database is None:
            print("Failed to build the inverted index. Exiting...")
            return
    except Exception as e:
        print(e)
        return

    print("The system is ready. Enter your text (#EXIT# to finish):")
    original_inp = ''

    while True:
        # Get sub sentence from the user
        original_inp, search_query = get_user_input(original_inp)

        if original_inp.endswith('#EXIT#'):
            print("Exiting...")
            break
        elif original_inp.endswith("#"):
            original_inp = ''
            continue

        # Measure the time taken to search
        start_time = time.time()  # TODO: del

        matches = dict_database.get_best_k_completions(search_query)

        print(f"Here are {len(matches)} suggestions")
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m}")

        end_time = time.time()  # TODO: del
        search_time = end_time - start_time  # TODO: del
        print(f"Search took {search_time:.4f} seconds")  # TODO: del


def get_user_input(user_input=''):
    print(f"{user_input}", end='', flush=True)
    new_input = input()
    user_input += new_input.strip() if not new_input.startswith(" ") else " " + new_input.strip()
    return user_input, Dictionary.normalize_line(user_input)


if __name__ == "__main__":
    sentence_completion(file_path)
    # cProfile.run('sentence_completion(file_path)')
