import re
from math import floor

import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


class TextSummarizer:

    def __init__(self):
        nltk.download("stopwords")

    def read_article(self, article):
        article_text = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', article)
        sentences = []

        for sentence in article_text:
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop() 
    
        return sentences

    def sentence_similarity(self, sent1, sent2, stopwords=None):
        if stopwords is None:
            stopwords = []
    
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
    
        all_words = list(set(sent1 + sent2))
    
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
    
        # build the vector for the first sentence
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] += 1
    
        # build the vector for the second sentence
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] += 1
    
        return 1 - cosine_distance(vector1, vector2)
 
    def build_similarity_matrix(self, sentences, stop_words):
        # Create an empty similarity matrix
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
    
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2: #ignore if both are same sentences
                    continue 
                similarity_matrix[idx1][idx2] = self.sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

        return similarity_matrix


    def generate_summary(self, article, percent):
        stop_words = stopwords.words('english')
        summarize_text = []

        # Step 1 - Read text anc split it
        sentences = self.read_article(article)
        top_n = int(floor(len(sentences) * int(100 - percent) * 0.01))
        if top_n == 0:
            top_n = 1

        # Step 2 - Generate Similary Martix across sentences
        sentence_similarity_martix = self.build_similarity_matrix(sentences, stop_words)

        # Step 3 - Rank sentences in similarity martix
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
        scores = nx.pagerank(sentence_similarity_graph)

        # Step 4 - Sort the rank and pick top sentences
        ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

        print(len(ranked_sentence), top_n)    

        for i in range(top_n):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

        # Step 5 - Offcourse, output the summarize text
        print("Summarize Text: \n", ". ".join(summarize_text))

        summarized_text = ". ".join(summarize_text)
        words = len(summarized_text.split())

        data = {
            'summarize': summarized_text,
            'words': words,
            'sentences': len(summarize_text),
            'readingTime': words // 5,
        }
        return data