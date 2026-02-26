!pip install gradio

import gradio as gr
import json

def gradio_search(query, intent_filter, sentiment_filter):
  intent_filter = None if intent_filter == 'Any' else intent_filter
  sentiment_filter = None if sentiment_filter == 'Any' else sentiment_filter

  report = build_report(
      query,
      top_k=20,
      intent = intent_filter,
      sentiment = sentiment_filter
  )

  bullets_text = '\n'.join(report['bullets'])
  themes_text = ', '.join(report.get('themes', []))

  evidence_df = pd.DataFrame(report['evidence'])[
      ['score', 'intent_label_final', 'sentiment_label', 'text_clean']
  ]

  return bullets_text, themes_text, evidence_df, json.dumps(report, indent=2)


#---

import gradio as gr
import pandas as pd
import json
import traceback
import matplotlib.pyplot as plt
import os, re, tempfile
from datetime import datetime

def _safe_slug(s: str, max_len=60):
    s = (s or "query").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:max_len] or "query"

def plot_trend(trend_df: pd.DataFrame):
    if trend_df is None or trend_df.empty:
        fig = plt.figure()
        plt.title("No trend data")
        return fig

    df = trend_df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    fig = plt.figure()
    for s, g in df.groupby("sentiment_label"):
        g = g.sort_values("date")
        plt.plot(g["date"], g["count"], label=str(s))

    plt.legend()
    plt.title("Query Trend (by sentiment)")
    plt.xlabel("date")
    plt.ylabel("count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    return fig


# --- SEARCH TAB logic (stores report in state, downloads on button) ---
def gradio_search(query, intent_filter, sentiment_filter, top_k):
    try:
        intent_filter = None if intent_filter == "Any" else intent_filter
        sentiment_filter = None if sentiment_filter == "Any" else sentiment_filter

        report = build_report(
            query,
            top_k=int(top_k),
            intent=intent_filter,
            sentiment=sentiment_filter
        )

        bullets_text = "\n".join(report.get("bullets", []))
        themes_text = ", ".join(report.get("themes", []))

        evidence_df = pd.DataFrame(report.get("evidence", []))
        if not evidence_df.empty:
            keep = [c for c in ["score","intent_label_final","sentiment_label","text_clean"] if c in evidence_df.columns]
            evidence_df = evidence_df[keep]

        trend_df = pd.DataFrame(report.get("trend", []))
        trend_plot = plot_trend(trend_df)

        report_json = json.dumps(report, indent=2)

        return bullets_text, themes_text, evidence_df, trend_plot, trend_df, report_json, report

    except Exception:
        err = traceback.format_exc()
        empty_plot = plot_trend(pd.DataFrame())
        return "ERROR", "", pd.DataFrame(), empty_plot, pd.DataFrame(), err, None


def download_report(report):
    if report is None:
        return None

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = _safe_slug(report.get("query", "query"))
    filename = f"insights_{ts}_{slug}.json"
    tmp_path = os.path.join(tempfile.gettempdir(), filename)

    with open(tmp_path, "w") as f:
        json.dump(report, f, indent=2)

    return tmp_path


# --- TRENDING TOPICS TAB logic ---
def gradio_trending(days_recent, days_base, min_base, top_n):
    try:
        trend_df, windows = compute_trending_topics(
            meta,
            topics_by_id,
            days_recent=int(days_recent),
            days_base=int(days_base),
            min_base=int(min_base),
            top_n=int(top_n)
        )

        win_text = (
            f"End: {windows['end']}\n"
            f"Recent window: {windows['start_recent']} → {windows['end']}  (last {days_recent} days)\n"
            f"Baseline window: {windows['start_base']} → {windows['start_recent']}  (prev {days_base} days)"
        )

        return trend_df, win_text
    except Exception:
        return pd.DataFrame(), traceback.format_exc()


def gradio_topic_examples(topic_id):
    try:
        if topic_id is None or str(topic_id).strip() == "":
            return ""
        ex = topic_examples(meta, int(topic_id), n=8)
        return "\n\n---\n\n".join(ex)
    except Exception:
        return traceback.format_exc()


with gr.Blocks() as demo:
    gr.Markdown("# Social Listening Insight Engine (Demo)")

    with gr.Tabs():
        # ---------------- SEARCH TAB ----------------
        with gr.Tab("Search"):
            state_report = gr.State(None)

            with gr.Row():
                query = gr.Textbox(label="Query", placeholder="e.g. delivery delay refund", scale=3)
                top_k = gr.Slider(5, 50, value=20, step=5, label="Top K (evidence shown)", scale=1)

            with gr.Row():
                intent_filter = gr.Dropdown(
                    ["Any","complaint","question","request","praise","conversation","sarcasm","other"],
                    value="Any",
                    label="Intent Filter"
                )
                sentiment_filter = gr.Dropdown(
                    ["Any","pos","neg","neutral"],
                    value="Any",
                    label="Sentiment Filter"
                )

            with gr.Row():
                search_btn = gr.Button("Run")
                download_btn = gr.Button("Download JSON")

            bullets_out = gr.Textbox(label="Summary", lines=5)
            themes_out = gr.Textbox(label="Themes")
            evidence_out = gr.Dataframe(label="Evidence", wrap=True)

            trend_plot_out = gr.Plot(label="Trend Chart")
            trend_table_out = gr.Dataframe(label="Trend Table", wrap=True)

            json_out = gr.Textbox(label="Raw JSON / Errors", lines=10)
            download_out = gr.File(label="Download File")

            search_btn.click(
                gradio_search,
                inputs=[query, intent_filter, sentiment_filter, top_k],
                outputs=[bullets_out, themes_out, evidence_out, trend_plot_out, trend_table_out, json_out, state_report]
            )

            download_btn.click(
                download_report,
                inputs=[state_report],
                outputs=[download_out]
            )

        # ---------------- TRENDING TOPICS TAB ----------------
        with gr.Tab("Trending Topics"):
            gr.Markdown("Shows topics rising in the recent window vs baseline (global, not query-only).")

            with gr.Row():
                days_recent = gr.Slider(3, 21, value=7, step=1, label="Recent window (days)")
                days_base   = gr.Slider(7, 90, value=30, step=1, label="Baseline window (days)")
                min_base    = gr.Slider(0, 200, value=15, step=1, label="Min baseline count (filter)")
                top_n       = gr.Slider(5, 50, value=15, step=5, label="Top N topics")

            trend_btn = gr.Button("Compute Trending Topics")

            windows_out = gr.Textbox(label="Windows used", lines=3)
            trending_table = gr.Dataframe(label="Trending topics", wrap=True)

            gr.Markdown("Pick a topic_id from the table and paste it below to see example posts.")
            topic_id_in = gr.Number(label="topic_id")
            examples_btn = gr.Button("Show examples")
            examples_out = gr.Textbox(label="Example posts", lines=14)

            trend_btn.click(
                gradio_trending,
                inputs=[days_recent, days_base, min_base, top_n],
                outputs=[trending_table, windows_out]
            )

            examples_btn.click(
                gradio_topic_examples,
                inputs=[topic_id_in],
                outputs=[examples_out]
            )

demo.launch(debug=True)
