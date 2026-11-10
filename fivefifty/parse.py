from fivefifty.loader import load_folder

def subject_and_body(raw):
    headers, _, body = raw.partition("\n\n")
    subject = ""
    split_header = headers.splitlines()
    for line in split_header:
        lower_line = line.lower()
        if lower_line.startswith("subject:"):
            _, _, text = lower_line.partition(":")
            subject = text.strip(" ")
            break
    return (subject + "\n" + body)

if __name__ == "__main__":
    spam = load_folder("./data/spam", "spam")
    text = spam[0][0]
    result = subject_and_body(text)
    print(result[:300])