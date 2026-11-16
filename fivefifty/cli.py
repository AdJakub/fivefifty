import sys
import argparse
from pathlib import Path

from fivefifty.classify import multinomial_classify, explain
from fivefifty.model import load_model, train_model, save_model


def check(text, model):

    classification = multinomial_classify(text, model["fractions"], model["email_counts"])
    return classification[0].upper()

def main():

    parser = argparse.ArgumentParser(prog="fivefifty", description="A spam filter you can read, that tells you why, and that learns from your own inbox")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check_parser = subparsers.add_parser("check", help="classify one email and show why")
    train_parser = subparsers.add_parser("train", help="train your own model on ham and spam")
    train_parser.add_argument("spam")
    train_parser.add_argument("ham")
    train_parser.add_argument("--out", default="my_model.json")
    check_parser.add_argument("email")
    check_parser.add_argument("--model")
    args = parser.parse_args()
    if args.command == "train":
        model = train_model(args.spam, args.ham)
        save_model(model, args.out)
        print(f"Trained on {model['email_counts']['spam']} spam and {model['email_counts']['ham']} ham. Saved to {args.out}")
    else:
        try:
            with open(args.email, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"{args.email} not found. Check for typos")
            sys.exit(1)
        if args.model:
            model_path = args.model
        else:
            model_path = Path(__file__).parent / "model.json"
        try:
            model = load_model(model_path)
        except FileNotFoundError:
            print(f"{model_path} not found. Check for typos.")
        verdict = check(text, model)
        print(verdict)
        explanation = explain(text, model['fractions'])
        ranked = sorted(explanation.items(), key=lambda pair: pair[1])
        if verdict == "SPAM":
            reasons = ranked[-5:][::-1]
        else:
            reasons = ranked[:5]
        print("="*20,"REASONING", "="*20)
        for word, push in reasons:
            print(f"{word:<10}:\t{push:+.1f}")

if __name__ == "__main__":
    main()