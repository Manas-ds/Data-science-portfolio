#using KMeans for clustering topics

from sklearn.cluster import KMeans

K = 20

kmeans = KMeans(n_clusters=K, random_state=51, n_init='auto')
topic_id = kmeans.fit_predict(X)

meta['topic_id'] = topic_id
print(meta['topic_id'].value_counts().head())

#TF-IDF keywords extraction

#keywords extraction per topic

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1,2),
    stop_words='english',
    min_df=5
)

T = tfidf.fit_transform(meta['text_clean'].fillna('').astype(str))
vocab = np.array(tfidf.get_feature_names_out())

def top_kw_for_topics(tid, topn=12):
  idx = np.where(meta['topic_id'].values == tid)[0]
  if len(idx)==0:
    return[]

  mean_vec = T[idx].mean(axis=0)
  mean_vex = np.asarray(mean_vec).ravel()
  top_idx = mean_vec.argsort()[::-1][:topn]
  return vocab[top_idx].tolist()

topic_keywords = {tid: top_kw_for_topics(tid, topn=12) for tid in range(K)}
topic_keywords


