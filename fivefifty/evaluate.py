from fivefifty.classify import classify, load_dataset, bernoulli_classify, make_bases
from fivefifty.train import count_words, make_fractions

def evaluate(test_list, classifier, model_a, model_b):
    results = {"caught": 0, "missed": 0, "false positive": 0, "correct ham": 0}
    classify = classifier
    for text, label in test_list:
        prediction, _ = classify(text, model_a, model_b)
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
    results = evaluate(test, classify, counts, email_counts)
    accuracy, precision, recall = metrics(results)
    print(f"{results}, {accuracy:.1%}, {precision:.1%}, {recall:.1%}")
    print("-"*40)
    fractions = make_fractions(counts, email_counts)
    bases = make_bases(fractions, email_counts)
    res_ber = evaluate(test, bernoulli_classify, fractions, bases)
    accuracy2, precision2, recall2 = metrics(res_ber)
    print(f"{res_ber}, {accuracy2:.1%}, {precision2:.1%}, {recall2:.1%}")
    print("-"*40)
    final_fractions = make_fractions(counts, email_counts, 112)
    final_bases = make_bases(final_fractions, email_counts)
    res_final = evaluate(test, bernoulli_classify, final_fractions, final_bases)
    accuracy3, precision3, recall3 = metrics(res_final)
    print(f"{res_final}, {accuracy3:.1%}, {precision3:.1%}, {recall3:.1%}")
