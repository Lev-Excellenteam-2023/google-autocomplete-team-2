from rapidfuzz import fuzz
import concurrent.futures
import Levenshtein


def is_partial_match(search_term, line, threshold=80):
    len_search = len(search_term)

    # if abs(len(line) - len_search) > 3:
    #     return False

    # if len(line) <= len_search:
    #     return False

    similarity = fuzz.ratio(search_term, line)
    # print(f"fuzz.ratio({search_term}, {line}) = {similarity}")
    # similarity = Levenshtein.ratio(search_term, line)
    # print(f"Levenshtein.ratio({search_term}, {line}) = {similarity}")

    if similarity >= threshold:
        # Check for exact length substrings (same length as search_term)
        for i in range(len(line) - len_search + 1):
            substring = line[i:i + len_search]
            if Levenshtein.distance(search_term, substring) <= 1:
                return substring

        # Check for substrings of length -1 (one character shorter)
        if len_search > 1:
            len_search_minus_one = len_search - 1
            for i in range(len(line) - len_search_minus_one + 1):
                substring = line[i:i + len_search_minus_one]
                if Levenshtein.distance(search_term, substring) <= 1:
                    return substring

        # Check for substrings of length +1 (one character longer)
        len_search_plus_one = len_search + 1
        for i in range(len(line) - len_search_plus_one + 1):
            substring = line[i:i + len_search_plus_one]
            if Levenshtein.distance(search_term, substring) <= 1:
                return substring
    return False


def is_partial_match_parallel(search_term, lines, threshold=80):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(is_partial_match, search_term, line, threshold): line for line in lines}
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    return results


def calculate_score(search_term, fuzzy_match):
    print(search_term, fuzzy_match)
    len_search = len(search_term)
    fuzzy_len = len(fuzzy_match)
    base_score = 2 * len_search

    incorrect_penalty = 0

    if len_search == fuzzy_len:
        for i in range(min(len_search, fuzzy_len)):
            if search_term[i].lower() != fuzzy_match[i].lower():
                if i == 0:
                    incorrect_penalty -= 5
                elif i == 1:
                    incorrect_penalty -= 4
                elif i == 2:
                    incorrect_penalty -= 3
                elif i == 3:
                    incorrect_penalty -= 2
                else:
                    incorrect_penalty -= 1

    else:
        if abs(len_search - fuzzy_len) == 1:
            for i in range(min(len_search, fuzzy_len)):
                if search_term[i].lower() != fuzzy_match[i].lower():
                    if i == 0:
                        incorrect_penalty -= 10
                    elif i == 1:
                        incorrect_penalty -= 8
                    elif i == 2:
                        incorrect_penalty -= 6
                    elif i == 3:
                        incorrect_penalty -= 4
                    else:
                        incorrect_penalty -= 2

    return base_score + incorrect_penalty


def process_search(search_term, lines, threshold=80):
    results = is_partial_match_parallel(search_term, lines, threshold)

    scored_results = [(result, calculate_score(search_term, result)) for result in results]

    scored_results.sort(key=lambda x: x[1], reverse=True)
    return scored_results
