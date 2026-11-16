import sys
from pathlib import Path

from fivefifty.classify import multinomial_classify, explain
from fivefifty.model import load_model


def check(text, model):

    classification = multinomial_classify(text, model["fractions"], model["email_counts"])
    return classification[0].upper()

def main():

    if len(sys.argv) < 2:
        print("Usage: fivefifty email.txt")
        sys.exit(1)
    else:
        with open(sys.argv[1], "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        model_path = Path(__file__).parent / "model.json"
        model = load_model(model_path)
        verdict = check(text, model)
        print(verdict)
        explanation = explain(text, model['fractions'])
        ranked = sorted(explanation.items(), key=lambda pair: pair[1])
        if verdict == "SPAM":
            print(ranked[-5:])
        else:
            print(ranked[:5])

if __name__ == "__main__":
    main()