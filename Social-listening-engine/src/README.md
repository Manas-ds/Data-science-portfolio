
---

## 🐍 **Source Code README (`/src/README.md`)**
# Source Code

Clean, modular version of the notebook code. Each file does one thing.

## Files

| File | What it does |
|------|--------------|
| `text_cleaner.py` | Strips mentions, URLs, punctuation from text |
| `intent_classifier.py` | Rules + zero-shot to label posts as complaint/question/etc |
| `vector_search.py` | Builds FAISS index and searches semantically |
| `topic_modeling.py` | Clusters posts + extracts keywords per topic |
| `trend_analysis.py` | Finds rising topics over time |
| `utils.py` | Helper functions (save/load, slugs, etc) |

## Usage example
```python
from src.text_cleaner import clean_for_topics
from src.vector_search import VectorSearch

# Clean some text
clean = clean_for_topics("Check out this #cool post @user")

# Search
searcher = VectorSearch()
searcher.load('index.faiss', 'meta.parquet')
results = searcher.search("delivery problems")
