
embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(embed_model_name)

TEXT_COL = "text_clean"

texts = events2[TEXT_COL].fillna("").astype(str).tolist()

emb = model.encode(
    texts,
    batch_size=256,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True,
).astype("float32")

n, d = emb.shape
print("Embeddings shape:", emb.shape)

index = faiss.IndexFlatIP(d)
index.add(emb)
print("FAISS index size:", index.ntotal)

faiss.write_index(index, INDEX_PATH)

meta_cols = [
    "event_id", "timestamp", "source",
    "sentiment_label", "intent_label_final", TEXT_COL
]
meta = events2[meta_cols].copy()
meta["row_id"] = np.arange(len(meta), dtype=np.int32)
meta.to_parquet(META_PATH, index=False)

print("Saved index + meta.")


# Search test

def search(query, k=10):
  q_emb = model.encode([query], normalize_embeddings = True, convert_to_numpy=True).astype('float32')
  scores, idxs = index.search(q_emb, k)
  hits = meta.iloc[idxs[0]].copy()
  hits['score'] = scores[0]
  return hits[['score', 'event_id', 'intent_label_final', 'sentiment_label', TEXT_COL]].head(k)

search('delivery delay refund not received', k=10)

