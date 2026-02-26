# we did 2 different cleaners
# 1. for starter use
import re

def clean_text_basic(s: str) -> str:
  s = s.strip()
  s = re.sub(r"\s+", " ", s)
  s = re.sub(r"http\S+|www\.\S+", "", s)
  s = re.sub(r"@\w+", "@user", s)
  s = s.replace("#", "")
  return s.strip()

events["text_clean"] = events['text'].map(clean_text_basic)
events[['text', 'text_clean']].sample(10, random_state=51)

# 2. When we were making topic analyser
import re

def clean_for_topics(s: str) -> str:
  s = (s or '').lower()
  s = re.sub(r"@\w+", " ", s)            # mentions
  s = re.sub(r"http\S+", " ", s)         # urls
  s = re.sub(r"#(\w+)", r" \1 ", s)       # keep hashtag word, drop '#'
  s = re.sub(r"[^a-z\s]", " ", s)         # letters + spaces only
  s = re.sub(r"\s+", " ", s).strip()
  return s

meta['text_for_topics'] = meta['text_clean'].map(clean_for_topics)
meta['text_for_topics'].head(10)
