from pathlib import Path
from pydoc import replace


def load_folder(path, label):
    path_loaded = Path(path)
    results = list()
    for entry in path_loaded.iterdir():
        entry_string = entry.read_text(encoding="utf-8", errors="replace")
        results.append((entry_string, label))
    return results


if __name__ == "__main__":
    results = load_folder("./data/spam", "spam")
    ez_ham = load_folder("./data/easy_ham", "ham")
    print (len(ez_ham), ez_ham[1][0])