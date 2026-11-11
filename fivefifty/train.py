from fivefifty.parse import subject_and_body
from fivefifty.tokenizer import tokenize
from fivefifty.split import load_dataset


def count_words(emails):
    counts = {"spam": {}, "ham": {}}
    email_counts = {"spam": 0, "ham": 0}
    for text, label in emails:
        email_counts[label] += 1
        words = tokenize(subject_and_body(text))
        for word in set(words):
            counts[label][word] = counts[label].get(word, 0) + 1
    return counts, email_counts

if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    counts, email_counts = count_words(train)
    print(email_counts)
    for word in ("click", "free", "patch"):
        print(f"{word}, spam: {counts['spam'].get(word, 0) / email_counts['spam']:.1%}, ham: {counts['ham'].get(word, 0) / email_counts['ham']:.1%}")