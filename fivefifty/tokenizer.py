def strip_tags(text):
    kept_chars = list()
    inside = False
    for char in text:
        if char == "<":
            inside = True
        elif char == ">":
            inside = False
            kept_chars.append(" ")
        elif not inside:
            kept_chars.append(char)
    return "".join(kept_chars)

def tokenize(text):
    text = strip_tags(text)
    text = text.lower()
    cleaned = list()
    for char in text:
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append(" ")
    return "".join(cleaned).split()

if __name__ == "__main__":
    from fivefifty.loader import load_folder
    from fivefifty.parse import subject_and_body
    spam = load_folder("./data/spam", "spam")
    email = spam[0][0]
    clean_email = subject_and_body(email)
    final = tokenize(clean_email)
    print(strip_tags("a<b>c</b>d"))
    print(strip_tags("no tags here"))
    print(strip_tags("<HTML><BODY>click here</BODY></HTML>"))
    print(strip_tags("if x < 5 then y > 2"))
    print(final[:60])

