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


def make_fractions(counts, email_counts):
    every_word = counts["spam"].keys() | counts["ham"].keys()
    fractions = {"spam": {}, "ham": {}}
    for label in ["spam", "ham"]:
        for word in every_word:
            label_counts = counts[label]
            word_count = label_counts.get(word, 0)
            fraction = (word_count + 1) / (email_counts[label] + 2)
            fractions[label][word] = fraction

    return fractions


if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    counts, email_counts = count_words(train)
    print(email_counts)
    for word in ("click", "free", "patch"):
        print(f"{word}, spam: {counts['spam'].get(word, 0) / email_counts['spam']:.1%}, ham: {counts['ham'].get(word, 0) / email_counts['ham']:.1%}")