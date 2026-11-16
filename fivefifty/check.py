import sys
from pathlib import Path

from fivefifty.classify import multinomial_classify
from fivefifty.model import load_model


def check(path):
    with open(path, "r",encoding="utf-8", errors="replace") as f:
        text = f.read()
    model_path = Path(__file__).parent / "model.json"
    model = load_model(model_path)
    classification = multinomial_classify(text, model["fractions"], model["email_counts"])
    return classification[0].upper()

def main():

    if len(sys.argv) < 2:
        print("Usage: fivefifty email.txt")
        sys.exit(1)
    else:
        print(check(sys.argv[1]))
if __name__ == "__main__":
    main()