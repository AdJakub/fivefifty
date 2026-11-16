# fivefifty

> A spam filter you can read, that tells you why, and that learns from your own inbox.


fivefifty is a tiny naive bayes spam filter, written from scratch. It utilizes no machine learning or non-standard libraries at all. I made it to learn about spam filters and provide a learning tool for others learning about spam filters.

## install
```
pip install fivefifty
```
or from source:
```
git clone https://github.com/AdJakub/fivefifty
cd fivefifty
pip install -e .
```
needs python 3.10+. zero dependencies, standard library only.

## use it
check one email (a `.eml` file, e.g. gmail → ⋮ → "Download message"):
```
fivefifty check some_email.eml
```
```
SPAM
[('payment', 12.719685971180983), ('le', 15.667823491997437), ('de', 19.956307904829593), ('les', 20.702822876133904), ('your', 26.43092106142582)]
```

train your own model on your own mail:
```
fivefifty train my_spam/ my_ham/ --out my_model.json
fivefifty check some_email.eml --model my_model.json
```
The built in model is based on mostly english 2002 spam. Training your own shows it modern spam in your own language

everything runs locally. no email ever leaves your machine.

## results
test set: 100 spam + 500 ham the filter never saw while training.

| version | spam caught | spam missed | real emails flagged | precision | recall |
|---|---|---|---|---|---|
| first try (bernoulli-ish, present words only) | 100 | 0 | 104 | 49.0% | 100% |
| bernoulli NB, all words | 21 | 79 | 5 | 80.8% | 21.0% |
| bernoulli NB, words seen in ≥112 emails | 84 | 16 | 14 | 85.7% | 84.0% |
| **multinomial NB + MIME decoding (final)** | **93** | **7** | **0** | **100%** | **93.0%** |

Accuracy isn't the main number to look at, the test set had more ham than spam emails, and saying ham always gives 83% accuracy.
## how it works
1. `parse.py`: unpacks the email (MIME: base64, quoted-printable, multipart), keeps subject + text parts. no headers, on purpose.
2. `tokenizer.py`: drops `<style>` blocks and html tags, lowercases, splits into words, drops "words" over 22 chars (base64 junk)
3. `train.py`: counts every word in spam and in ham, turns counts into smoothed fractions
4. `classify.py`: multinomial naive bayes, adds up log-evidence for every word in the email. `explain()` shows which words pushed hardest.
5. `evaluate.py`: caught / missed / false positives, precision, recall
6. `cli.py`: the `fivefifty` command


The filter started out as a bernoulli naive bayes filter. However ham started 216 points ahead because of 35k junk words and it only had good results when cutting a very large part of the vocabulary. That's when the filter was switched to a multinomial algorithm instead. A large vocabulary base does not hurt multinomial naive bayes algorithms.

## how it was measured
- emails split into train (2400) and test (600), spam and ham split separately, seeded
- train split again into fit (1920) + validation (480) for every choice i made (like N for bernoulli)
- test was only used to report final numbers once per model, plus once more after adding MIME decoding (a decision made on validation, not on test)
- the model shipped in the package is trained on all 3000 emails 

## what it found along the way
- 64% of the vocabulary was words seen in exactly one email (mostly base64 junk)
- bernoulli NB works best with a tiny vocabulary (~1%), multinomial doesnt care. matches McCallum & Nigam (1998)
- on a real 2026 phishing email, french "poisoning" text backfired: french words look spammy to a filter trained on 2002 email

## limitations 
- trained on the 2002 SpamAssassin corpus. modern spam is different, so train your own for real use.
- only english-ish easy_ham was measured. hard_ham (newsletters, html-heavy) not evaluated yet.
- 0 false positives in 500 means the real rate is probably under ~0.6% (rule of three), not zero
- some mailing lists break base64 bodies by appending footers. those cant be decoded.
- no learning from corrections yet



## data
built and measured on the [SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/) (`20021010_spam`, `20021010_easy_ham`, `20021010_hard_ham`).
to reproduce: extract into `data/spam`, `data/easy_ham`, `data/hard_ham`, then `python -m fivefifty.evaluate` from the repo root.

## license
MIT