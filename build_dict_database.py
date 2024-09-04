import re
import time
import zipfile
from collections import defaultdict

from position import Position


def build_dict(zip_file_path):
    data_dict = defaultdict(list)

    print("Build starting now")  # TODO: del
    start_time = time.time()  # TODO: del

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith('.txt'):
                    with zip_ref.open(file_name) as file:
                        for line_number, line in enumerate(file, 1):
                            line = line.decode('utf-8').strip()
                            normalized_line = normalize_line(line)
                            if normalized_line:
                                data_dict[normalized_line].append(Position(line, file_name, line_number))

        end_time = time.time()  # TODO: del
        search_time = end_time - start_time  # TODO: del
        print(f"Building took {search_time:.4f} seconds\n")  # TODO: del

    except zipfile.BadZipFile:
        raise zipfile.BadZipFile(f"The file '{zip_file_path}' is not a valid ZIP file.")

    except Exception as e:
        raise Exception(f"An error occurred while processing the file '{zip_file_path}': {str(e)}")

    return data_dict


def normalize_line(line):
    return ' '.join(re.findall(r'[a-zA-Z0-9]+', line.lower()))
