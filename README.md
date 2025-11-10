# Whatsapp-statistics

This repository contains Python utilities to parse a WhatsApp chat export and generate a set of exploratory charts and tables about message activity and content.

> **Status:** work‑in‑progress. A feature for parsing english whatsapp chats still needs to be developed.

---

## Features

- **Activity over time** – messages per day/week/month and moving averages
- **Who talks most** – messages, words, and media sent by participant
- **Daily and hourly rhythms** – heatmaps by weekday/hour
- **Top content** – most common words/phrases (stopwords filtered), emojis, links

> The exact plots depend on the functions under `utils/`.

---

## Project structure

```
Whatsapp-statistics/
├─ main.py           # CLI entry point to run analyses and save charts
├─ utils/            # parsing, cleaning, plotting helpers
└─ .gitignore
```

---


## Get a chat export

From the WhatsApp app:

1. Open the chat you want to analyze.
2. **More** → **Export chat** without media.
3. Save the `.txt` file to your computer (UTF‑8 plain text).

---

### How to run it

python main.py --data DATA_DIR
