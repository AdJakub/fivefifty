import math
from fivefifty.parse import subject_and_body
from fivefifty.tokenizer import tokenize
from fivefifty.classify import load_dataset, count_words, base_score, fast_score, make_bases, bernoulli_classify, multinomial_classify
from fivefifty.train import make_fractions, count_occurrences, make_multi_fractions
def lean(spam_count, ham_count, spam_mails, ham_mails):
    spam_fraction = (spam_count + 1) / (spam_mails + 2)
    ham_fraction = (ham_count + 1)  / (ham_mails + 2)
    return math.log(spam_fraction) - math.log(ham_fraction)
from fivefifty.split import train_test_split
from fivefifty.evaluate import evaluate, metrics


def bernoulli_score(prior, fractions, email_words):
    score = math.log(prior)
    for (word, fraction) in fractions.items():
        if word in email_words:
            score += math.log(fraction)
        else:
            score += math.log(1-fraction)
    return score



if __name__ == "__main__":
    # for n in range(8):
    #     lean_result = lean(0, n, 400, 2000)
    #     if lean_result > 0:
    #         classification = "Spam"
    #     else:
    #         classification = "Ham"
    #     print(n, f"{lean_result:.3f}\nClassification: {classification}")
    # print("="*40)
    # spam_fractions = {"click": 0.51, "free": 0.48, "patch": 0.01}
    # ham_fractions = {"click": 0.17, "free": 0.13, "patch": 0.02}
    # email_words = set({"click", "free"})
    # x = bernoulli_score(400/2400, spam_fractions, email_words)
    # y = bernoulli_score(2000/2400, ham_fractions, email_words)
    # print(f"X = {x}, Y = {y}")
    # if x > y:
    #     print("x wins!")
    # else:
    #     print("Y wins!")
    # print("="*40)
    # spam_base = base_score(400/2400, spam_fractions)
    # ham_base = base_score(2000/2400, ham_fractions)
    # fast_spam = fast_score(spam_base, spam_fractions, email_words)
    # fast_ham = fast_score(ham_base, ham_fractions, email_words)
    # print(f"X: {fast_spam}\nY: {fast_ham}")
    # print("="*40)
    train, test = load_dataset(0.2, 42)
    # counts, email_counts = count_words(train)
    # fractions = make_fractions(counts, email_counts)
    # print (f"Spam: {len(fractions['spam'])}\nHam: {len(fractions['ham'])}.")
    # for word in ("click", "free", "patch"):
    #     print(
    #         f"{word}, spam: {fractions['spam'][word]:.1%}, ham: {fractions['ham'][word]:.1%}")
    # train_email_total = sum(email_counts.values())
    # spam_prior = (email_counts['spam'] / train_email_total)
    # spam_base_result = base_score(spam_prior, fractions['spam'])
    # ham_prior = (email_counts['ham'] / train_email_total)
    # ham_base_result = base_score(ham_prior, fractions['ham'])
    # print('-'*40)
    # print(f'Spam base result: {spam_base_result}\nHam Base result: {ham_base_result}')
    # for text, label in test[:1]:
    #     subjected = subject_and_body(text)
    #     tokenized = tokenize(subjected)
    #     setted = set(tokenized)
    #     print(f"{label}, uniq words: {len(setted)}")
    #     spam_slow = bernoulli_score(spam_prior, fractions['spam'], setted)
    #     spam_fast = fast_score(spam_base_result, fractions['spam'], setted)
    #     print('-'*40)
    #     print(f'spam_slow: {spam_slow}, spam_fast: {spam_fast}')
    #     ham_slow = bernoulli_score(ham_prior, fractions['ham'], setted)
    #     ham_fast = fast_score(ham_base_result, fractions['ham'], setted)
    #     print('-'*40)
    #     print(f"ham_slow: {ham_slow}, ham_fast: {ham_fast}")
    #     print("-"*40)
    #     bases = make_bases(fractions,email_counts)
    #     bern_res = bernoulli_classify(text, fractions, bases)
    #     print("-"*40)
    #     print(bern_res)
    #     only_one = 0
    #     only_one_email_words = list()
    #     for word in fractions['spam']:
    #         total = counts['ham'].get(word, 0) + counts['spam'].get(word, 0)
    #         if total == 1:
    #             only_one_email_words.append(word)
    #             only_one += 1
    #     print(only_one)
    #     print(only_one_email_words[:30])
    fit, val = train_test_split(train, 0.2, 42,)
        # print(len(fit), len(val))
        # fractions2 = make_fractions(counts, email_counts, 2)
        # print(len(fractions2['spam']), len(fractions2['ham']))
    fit_counts, fit_email_counts = count_words(fit)
        # print(fit_email_counts)
        ###### TRYING SEVERAL N
    print("-"*40)
    for n in [1, 2, 5, 10, 20, 50, 90]:
        fit_fractions = make_fractions(fit_counts, fit_email_counts, n)
        fit_bases = make_bases(fit_fractions, fit_email_counts)
        evaluation = evaluate(val, bernoulli_classify, fit_fractions, fit_bases)
        accuracy, precision, recall = metrics(evaluation)
        print(f"{n}, {evaluation}, precision: {precision:.1%}, recall: {recall:.1%}, vocab size: {len(fit_fractions['spam'])}")
    print("-"*40)
    counts,_,word_totals = count_occurrences(fit)
    print(word_totals)
    print(counts['spam'].get('free', 0))
    print("-"*40)
    multi_counts, multi_email_counts, multi_word_totals = count_occurrences(fit)
    multi_fractions = make_multi_fractions(multi_counts, multi_word_totals)
    multi_evaluation = evaluate(val, multinomial_classify, multi_fractions, multi_email_counts)
    multi_accuracy, multi_precision, multi_recall = metrics(multi_evaluation)
    print(
        f"multinomial, {multi_evaluation}, precision: {multi_precision:.1%}, recall: {multi_recall:.1%}, vocab size: {len(multi_fractions)}")
