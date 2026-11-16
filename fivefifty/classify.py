import math
from fivefifty.parse import subject_and_body
from fivefifty.tokenizer import tokenize
from fivefifty.split import load_dataset
from fivefifty.train import count_words

def base_score(prior, fractions):
    score = math.log(prior)
    for (word, fraction) in fractions.items():
        score += math.log(1 - fraction)
    return score

def fast_score(base, fractions, words):
    score = base
    for word in words:
        if word in fractions:
            fraction = fractions[word]
            score += math.log(fraction) - math.log(1 - fraction)
    return score

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

def make_bases(fractions, email_counts):
    train_email_total = sum(email_counts.values())
    bases = {}
    for label in ["spam", "ham"]:
        prior = (email_counts[label] / train_email_total)
        base = base_score(prior, fractions[label])
        bases[label] = base
    return bases

def bernoulli_classify(raw_text, fractions, bases):
    subjected = subject_and_body(raw_text)
    tokenized = tokenize(subjected)
    setted = set(tokenized)
    scores = {}
    for label in ["spam", "ham"]:
        scores[label] = fast_score(bases[label], fractions[label], setted)
    if scores["spam"] > scores["ham"]:
        return "spam", scores
    else:
        return "ham", scores

def multinomial_classify(raw_text, fractions, email_counts):
    subjected = subject_and_body(raw_text)
    tokenized = tokenize(subjected)
    train_email_total = sum(email_counts.values())
    scores = dict()
    for label in ["spam", "ham"]:
        score = math.log(email_counts[label] / train_email_total)
        for word in tokenized:
           if word in fractions[label]:
               score += math.log(fractions[label][word])
        scores[label] = score
    if scores["spam"] > scores["ham"]:
        return "spam", scores
    else:
        return "ham", scores

def explain(raw_text, fractions):
    subjected = subject_and_body(raw_text)
    tokenized = tokenize(subjected)
    pushes = dict()
    for token in tokenized:
        if token not in fractions["spam"]:
            continue
        push = math.log(fractions["spam"][token]) - math.log(fractions["ham"][token])
        pushes[token] = pushes.get(token, 0) + push
    return pushes
if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    counts, email_counts = count_words(train)
    for text, label in test[:10]:
        classification, score = classify(text, counts, email_counts)
        print(f"Real label: {label}\nPrediction: {classification}\nScore: {score}\n")

