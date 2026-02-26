# Data

Small sample files so you can test the code without downloading the full dataset.

## 📁 Files
- `sample_events.parquet` — 100 rows of processed posts with labels (coming soon)

## 📝 Schema
| Column | Description |
|--------|-------------|
| `event_id` | Unique ID |
| `text` | Raw tweet |
| `text_clean` | Cleaned version |
| `timestamp` | When it happened (synthetic) |
| `source` | Where it came from (tweet_eval) |
| `sentiment_label` | pos/neg/neutral |
| `intent_label_final` | complaint/question/praise/etc |
| `topic_id` | Which topic cluster it belongs to |

## 🔍 Full dataset
The notebook loads the complete tweet_eval dataset (45k posts) from Hugging Face.
These samples are just for quick testing.

## ⚠️ Note
Timestamps are synthetic (marked as such in the notebook).
Real data would come from Reddit/Meta APIs.
