import random
from fivefifty.loader import load_folder


def train_test_split(emails, test_fraction, seed):
    emails_list = list(emails)
    random.seed(seed)
    random.shuffle(emails_list)
    cut = int(len(emails_list) * (1 - test_fraction))
    train = emails_list[:cut]
    test = emails_list[cut:]
    return train, test

def load_dataset(test_fraction, seed):
    spam = load_folder("./data/spam", "spam")
    ham = load_folder("./data/easy_ham", "ham")
    spam_train, spam_test = train_test_split(spam, test_fraction, seed)
    ham_train, ham_test = train_test_split(ham, test_fraction, seed)
    train = spam_train + ham_train
    test = spam_test + ham_test
    return train, test
if __name__ == "__main__":
    train, test = load_dataset(0.2, 42)
    print(f"train: {len(train)}, test: {len(test)}")