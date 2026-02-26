# save_json()  - Save any dict as JSON
# load_json()  - Load JSON file back
# safe_slug()  - Turn "Hello World!" into "hello-world" for filenames
# themes_from_hits() - Find top keywords in search results
# trend_from_hits()  - Group posts by date for trend charts
# topic_examples()   - Get sample posts from a topic

import json
import pandas as pd
import numpy as np
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# ------------------------------------------------------------
# FILE HANDLING
# ------------------------------------------------------------

def save_json(data, path):
    """Save any dict/list as JSON file"""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_json(path):
    """Load JSON file"""
    with open(path, 'r') as f:
        return json.load(f)


# ------------------------------------------------------------
# TEXT UTILS
# ------------------------------------------------------------

def safe_slug(s: str, max_len=60) -> str:
    """Convert string to filename-friendly slug (e.g., 'My Query!' → 'my-query')"""
    s = (s or "query").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len] or "query"


# ------------------------------------------------------------
# THEMES FROM SEARCH RESULTS
# ------------------------------------------------------------

def themes_from_hits(hits_df, top_terms=12):
    """Extract top TF-IDF terms from a dataframe of posts"""
    col = "text_for_topics" if "text_for_topics" in hits_df.columns else "text_clean"
    texts = hits_df[col].fillna("").astype(str).tolist()
    
    if not texts:
        return []
    
    v = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1,2),
        max_features=8000
    )
    M = v.fit_transform(texts)
    vocab = np.array(v.get_feature_names_out())
    scores = np.asarray(M.mean(axis=0)).ravel()
    top_idx = scores.argsort()[::-1][:top_terms]
    
    return vocab[top_idx].tolist()


# ------------------------------------------------------------
# TREND FROM HITS
# ------------------------------------------------------------

def trend_from_hits(hits_df, freq="D"):
    """Create daily trend DataFrame grouped by sentiment"""
    if "timestamp" not in hits_df.columns or hits_df.empty:
        return pd.DataFrame()
    
    df = hits_df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    
    df["date"] = df["timestamp"].dt.floor(freq)
    
    trend = (
        df.groupby(["date", "sentiment_label"])
          .size()
          .reset_index(name="count")
          .sort_values("date")
    )
    
    return trend


# ------------------------------------------------------------
# TOPIC EXAMPLES (for trending topics tab)
# ------------------------------------------------------------

def topic_examples(meta, topic_id, n=8, seed=42):
    """Get random sample posts for a given topic"""
    df = meta[meta["topic_id"] == int(topic_id)].copy()
    if df.empty:
        return []
    df = df.sample(min(n, len(df)), random_state=seed)
    return df["text_clean"].fillna("").astype(str).tolist()
