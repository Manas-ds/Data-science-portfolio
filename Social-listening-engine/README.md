# Social Listening Engine

A tool that digs through social media posts to figure out what people are actually talking about — complaints, questions, trends, the works.

## 🎯 What it does
- Cleans up messy social media text
- Spots if someone's complaining, asking, or just chatting
- Lets you search posts by meaning (not just keywords)
- Groups conversations into topics
- Shows what's trending right now

## 🗂️ What's inside
📁 notebooks/ # Jupyter notebook with the full pipeline
📁 src/ # Clean Python modules (same code, better organized)
📁 app/ # Gradio web app
📁 data/ # Sample data to try things out


## 🚀 Quick start
```bash
# Install stuff
pip install -r requirements.txt

# Run the notebook
jupyter notebook notebooks/social_listening_engine.ipynb

# Or launch the web app
python app/gradio_app.py
```
📦 Built with

  - Python, pandas, numpy

  - Transformers, sentence-transformers

  - FAISS for fast search

  - scikit-learn for topics

  - Gradio for the UI

📄 License

MIT


