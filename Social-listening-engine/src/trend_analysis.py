# creating topic trend function
def trend_topics(days_recent=3, days_baseline=14, top_n=10):
  df = meta.copy()
  df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
  df = df.dropna(subset=['timestamp', 'topic_id'])
  df['day'] = df['timestamp'].dt.floor('D')

  last_day = df['day'].max()
  recent_start = last_day - pd.Timedelta(days=days_recent-1)
  base_start = last_day - pd.Timedelta(days=days_recent+days_baseline)
  base_end = last_day - pd.Timedelta(days = days_recent)

  daily = df.groupby(['day', 'topic_id']).size().reset_index(name='n')

  recent = daily[daily["day"] >= recent_start].groupby("topic_id")["n"].sum()
  base   = daily[(daily["day"] >= base_start) & (daily["day"] <= base_end)].groupby("topic_id")["n"].sum()

  trend = pd.DataFrame({"recent": recent, "baseline": base}).fillna(0)
  trend["trend_score"] = (trend["recent"] + 1) / (trend["baseline"] + 1)  # stable ratio
  trend = trend.sort_values("trend_score", ascending=False).head(top_n).reset_index()

  # attach keywords
  trend["keywords"] = trend["topic_id"].map(lambda tid: topics_by_id.get(int(tid), {}).get("keywords", [])[:8])
  return trend


#----


trend_topics(top_n=10)

import pandas as pd
import numpy as np

def compute_trending_topics(meta, topics_by_id, days_recent=7, days_base=30, min_base=15, top_n=15):
    df = meta.copy()
    df = df.dropna(subset=["topic_id", "timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    end = df["timestamp"].max()
    start_recent = end - pd.Timedelta(days=days_recent)
    start_base = start_recent - pd.Timedelta(days=days_base)

    recent = df[(df["timestamp"] >= start_recent) & (df["timestamp"] <= end)]
    base   = df[(df["timestamp"] >= start_base) & (df["timestamp"] < start_recent)]

    recent_counts = recent["topic_id"].value_counts()
    base_counts   = base["topic_id"].value_counts()

    out = []
    for tid, rc in recent_counts.items():
        bc = int(base_counts.get(tid, 0))
        if bc < min_base:
            continue

        # rate-normalized lift (so windows can differ)
        recent_rate = rc / max(days_recent, 1)
        base_rate   = bc / max(days_base, 1)
        lift = recent_rate / (base_rate + 1e-9)

        kw = topics_by_id.get(int(tid), {}).get("keywords", [])
        if isinstance(kw, list) and len(kw) == 1 and isinstance(kw[0], list):
            kw = kw[0]
        kw = ", ".join([str(x) for x in kw[:8]])

        out.append({
            "topic_id": int(tid),
            "lift": float(lift),
            "recent_count": int(rc),
            "base_count": int(bc),
            "keywords": kw
        })

    res = pd.DataFrame(out)
    if res.empty:
        return res, {"end": end, "start_recent": start_recent, "start_base": start_base}

    res = res.sort_values(["lift", "recent_count"], ascending=False).head(top_n).reset_index(drop=True)
    return res, {"end": end, "start_recent": start_recent, "start_base": start_base}


def topic_examples(meta, topic_id, n=8, seed=42):
    df = meta[meta["topic_id"] == int(topic_id)].copy()
    if df.empty:
        return []
    df = df.sample(min(n, len(df)), random_state=seed)
    return df["text_clean"].fillna("").astype(str).tolist()
