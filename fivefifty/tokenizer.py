def strip_style(text):
    while "<style" in text:
        before, _, rest = text.partition("<style")
        _,_,after = rest.partition("</style>")
        text = before + " " + after
    return text

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
    text = text.lower()
    text = strip_style(text)
    text = strip_tags(text)

    cleaned = list()
    kept = list()
    for char in text:
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append(" ")

    cleaned_pre_min_n =  "".join(cleaned).split()

    for token in cleaned_pre_min_n:
        if len(token) <= 22:
            kept.append(token)

    return kept

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
    print(strip_style("hello <style>p{font-size:47pt}</style> world"))
    print(strip_style("no style here"))
    print (strip_style("one <style>a</style> two <style>b</style> three"))
    test1 = tokenize("<STYLE>p{font-size:47pt}</STYLE> Hello World")
    print(tokenize("kptrtve1xpposcsgsu71sdd, counterrevolutionaries"))
    print (test1)
    print(final[:60])

