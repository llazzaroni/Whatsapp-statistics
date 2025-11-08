import re

word_rx = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")
def tokenize(s: str):
    if not isinstance(s, str):
        return []
    return [w.lower() for w in word_rx.findall(s)]