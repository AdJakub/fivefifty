import math
from fivefifty.parse import subject_and_body
from fivefifty.tokenizer import tokenize
from fivefifty.split import load_dataset
from fivefifty.train import count_words


def classify(raw_text, counts, email_counts):
    subjected = subject_and_body(raw_text)
    tokenized = tokenize(subjected)
    setted = set(tokenized)
    train_email_total = sum(email_counts.values())
    scores = dict()
    for label in ["spam", "ham"]:
        score = math.log(email_counts[label] / train_email_total )
        for word in setted:
            if word not in counts["spam"] and word not in counts["ham"]:
                continue
            label_counts = counts[label]
            word_count = label_counts.get(word, 0)
            fraction = (word_count + 1) / (email_counts[label] + 2)
            score += math.log(fraction)
        scores[label] = score
    if scores["spam"] > scores["ham"]:
        return "spam", scores
    else:
        return "ham", scores



if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    counts, email_counts = count_words(train)
    for text, label in test[:10]:
        classification, score = classify(text, counts, email_counts)
        print(f"Real label: {label}\nPrediction: {classification}\nScore: {score}\n")

