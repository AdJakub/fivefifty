import json

from fivefifty.loader import load_folder
from fivefifty.train import count_occurrences, make_multi_fractions


def train_model():
    spam = load_folder("./data/spam", "spam")
    ez_ham = load_folder("./data/easy_ham", "ham")
    together = list(spam + ez_ham)
    counts, email_counts, word_totals = count_occurrences(together)
    multi_fractions = make_multi_fractions(counts, word_totals)
    return ({"fractions": multi_fractions, "email_counts": email_counts})

def save_model(model, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(model, f)

def load_model(path):
    with open(path, encoding="utf-8") as f:
       model = json.load(f)
    return model

if __name__ == "__main__":
    model = train_model()
    save_model(model, "model.json")
    loaded = load_model("model.json")
    print(loaded == model, len(loaded["fractions"]["spam"]))