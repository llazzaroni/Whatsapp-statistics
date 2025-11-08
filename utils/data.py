import unicodedata
import re
import pandas as pd

def strip_invisibles(s: str) -> str:
    return "".join(ch for ch in s if unicodedata.category(ch) != "Cf")

def load_messages_json(path):
    # Load the lines
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        raw_lines = f.read().splitlines()

    # Remove ‎
    lines = [strip_invisibles(x) for x in raw_lines]

    header_rx = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s*'          # date
        r'(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*'       # time (HH:MM[:SS])
        r'([^:]+):\s*'                              # sender (up to colon)
        r'(.*)$'                                    # text (rest of line)
    )

    messages = []  # list of dicts: {date, time, sender, text}
    curr = None

    for line in lines:
        m = header_rx.match(line)
        if m:
            date_str, time_str, sender, text = m.groups()
            curr = {"date": date_str, "time": time_str, "sender": sender.strip(), "text": text}
            messages.append(curr)
        else:
            if curr is not None:
                curr["text"] += "\n" + line

    omit_rx = re.compile(
        r'(?i)^\s*(?:<\s*media\s+omessi\s*>|<\s*messaggio\s+eliminato\s*>|'
        r'messaggio\s+eliminato|<\s*media\s+omitted\s*>|media\s+omitted|'
        r'image\s+omitted|audio\s+omitted|video\s+omitted|sticker\s+omitted|gif\s+omitted)\s*$'
    )
    messages = [m for m in messages if not omit_rx.match(m["text"].strip())]

    return messages

def load_messages_pd(path):
    messages = load_messages_json(path)
    messages = pd.DataFrame(messages)
    return messages