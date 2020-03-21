import heapq
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import nltk
import numpy as np
import networkx as nx
import re

file_name = 'test.txt'
file = open(file_name, "r",encoding='UTF-8')
filedata = file.read()
sentences = []
sentences = re.sub("[^a-zöüäA-ZÖÜÄ]", " ",filedata)
sentence_list = nltk.sent_tokenize(filedata)
stopwords = nltk.corpus.stopwords.words('german')
word_frequencies = {}
for word in nltk.word_tokenize(sentences):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1
maximum_frequncy = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)
