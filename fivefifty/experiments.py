import math


def lean(spam_count, ham_count, spam_mails, ham_mails):
    spam_fraction = (spam_count + 1) / (spam_mails + 2)
    ham_fraction = (ham_count + 1)  / (ham_mails + 2)
    return math.log(spam_fraction) - math.log(ham_fraction)


def bernoulli_score(prior, fractions, email_words):
    score = math.log(prior)
    for (word, fraction) in fractions.items():
        if word in email_words:
            score += math.log(fraction)
        else:
            score += math.log(1-fraction)
    return score

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

if __name__ == "__main__":
    for n in range(8):
        lean_result = lean(0, n, 400, 2000)
        if lean_result > 0:
            classification = "Spam"
        else:
            classification = "Ham"
        print(n, f"{lean_result:.3f}\nClassification: {classification}")
    print("="*40)
    spam_fractions = {"click": 0.51, "free": 0.48, "patch": 0.01}
    ham_fractions = {"click": 0.17, "free": 0.13, "patch": 0.02}
    email_words = set({"click", "free"})
    x = bernoulli_score(400/2400, spam_fractions, email_words)
    y = bernoulli_score(2000/2400, ham_fractions, email_words)
    print(f"X = {x}, Y = {y}")
    if x > y:
        print("x wins!")
    else:
        print("Y wins!")
    print("="*40)
    spam_base = base_score(400/2400, spam_fractions)
    ham_base = base_score(2000/2400, ham_fractions)
    fast_spam = fast_score(spam_base, spam_fractions, email_words)
    fast_ham = fast_score(ham_base, ham_fractions, email_words)
    print(f"X: {fast_spam}\nY: {fast_ham}")