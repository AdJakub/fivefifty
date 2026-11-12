from fivefifty.classify import classify, load_dataset
from fivefifty.train import count_words

def evaluate(test_list, counts, email_counts):
    results = {"caught": 0, "missed": 0, "false positive": 0, "correct ham": 0}
    for text, label in test_list:
        prediction, _ = classify(text, counts, email_counts)
        if prediction == "spam" and label == "spam":
            results["caught"] += 1
        elif prediction == "ham" and label == "spam":
            results["missed"] += 1
        elif prediction == "spam" and label == "ham":
            results["false positive"] += 1
        else:
            results["correct ham"] += 1

    return results

def metrics(results):
    total_unsummed = results.values()
    total = sum(total_unsummed)
    accuracy = (results["caught"] + results["correct ham"]) / total
    precision_bottom = results["caught"] + results["false positive"]
    if precision_bottom == 0:
        precision = 0
    else:
        precision = results["caught"] / precision_bottom
    recall_bottom = results["caught"] + results["missed"]
    if recall_bottom == 0:
        recall = 0
    else:
        recall = results["caught"] / recall_bottom
    return accuracy, precision, recall
if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    counts, email_counts = count_words(train)
    results = evaluate(test, counts, email_counts)
    accuracy, precision, recall = metrics(results)
    print(f"{results}, {accuracy:.1%}, {precision:.1%}, {recall:.1%}")