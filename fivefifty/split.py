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

if __name__ == "__main__":
    spam = load_folder("./data/spam", "spam")
    train, test = train_test_split(spam, 0.2, 42)
    print(f"train: {len(train)}, test:{len(test)}")
    print(train[0][:80])