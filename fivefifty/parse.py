import email

from fivefifty.loader import load_folder

def subject_and_body_old(raw):
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

def subject_and_body(raw):
    message = email.message_from_string(raw)
    subject = message["Subject"]
    if subject is None:
        subject = ""
    kept = list()
    kept.append(subject)
    for part in message.walk():
        content_type = part.get_content_type()
        if content_type.startswith("text/"):
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset()
            if payload == None:
                continue
            if charset == None:
                charset = "latin-1"
            try:
                decoded = payload.decode(charset, errors="replace")
            except LookupError:
                decoded = payload.decode('latin-1', errors="replace")

            kept.append(decoded)
    return "\n".join(kept)
if __name__ == "__main__":
    spam = load_folder("./data/spam", "spam")
    text = spam[0][0]
    result = subject_and_body(text)
    print(result[:300])