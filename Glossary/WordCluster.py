import collections

import gensim.downloader as api
from nltk import word_tokenize
import pickle
import numpy as np
from nltk.stem import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint

# model = api.load("glove-twitter-25")
# file = open('EnvCanadaGloss.txt', 'rb')
# file = file.read().splitlines()
# file = [model[line] for line in file]

emb = pickle.load(open("saveEmbeddings.pkl", "rb"))

# def process_text(text, stem=True):
#     tokens = word_tokenize(text)
#
#     if stem:
#         stemm = PorterStemmer()
#         tokens = [stemm.stem(t) for t in tokens]
#
#     return tokens
#
# def cluster_texts(texts, clusters=5):
#     vect = TfidfVectorizer(tokenizer=process_text, max_df=0.5, min_df=0.1, lowercase=True)
#     tfidf_model = vect.fit_transform(texts)
#
#
#     value = [v for k,v in emb.items()]
#
#
#     km_model = KMeans(n_clusters=clusters)
#     km_model.fit(value)
#
#     clustering = collections.defaultdict(list)
#
#     for idx, label in enumerate(km_model.labels_):
#         clustering[label].append(texts[idx])
#     return clustering


value = np.array([np.array(v) for k,v in emb.items()])
labels = [k for k,v in emb.items()]
km_model = KMeans(n_clusters=7)
km_model.fit(value)

clustering = collections.defaultdict(list)
print clustering

for idx, label in enumerate(km_model.labels_):
    clustering[label].append(labels[idx])

print clustering
