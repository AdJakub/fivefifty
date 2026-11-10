from pathlib import Path
from pydoc import replace


def load_folder(path, label):
    path_loaded = Path(path)
    results = list()
    for entry in path_loaded.iterdir():
        entry_string = entry.read_text(encoding="utf-8", errors="replace")
        results.append((entry_string, label))
    return results

def count_html(emails):
    counter = 0
    for text, label in emails:
        if "<html" in text.lower():
            counter += 1
    return counter

if __name__ == "__main__":
    spam = load_folder("./data/spam", "spam")
    ez_ham = load_folder("./data/easy_ham", "ham")
    hard_ham = load_folder("./data/hard_ham", "hard_ham")
    s_results = (count_html(spam) / len(spam))
    e_results = (count_html(ez_ham) / len(ez_ham))
    h_results = (count_html(hard_ham)/ len(hard_ham))
    print(f"s_results: {s_results:%}, ez_ham: {e_results:%}, hard_ham: {h_results:%}")

