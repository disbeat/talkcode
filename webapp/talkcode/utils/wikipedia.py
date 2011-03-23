import wikipedia as wiki
import re, sys

from heapq import nlargest
from operator import itemgetter

from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem.porter import PorterStemmer

stopwords = nltk_stopwords.words('english')
stemmer = PorterStemmer()


def get_related_wikipedia_words(query):
    pages = wiki.opensearch(query)
    if pages[1]:
        page_id = pages[1][0]
        content = wiki.query_text_raw(page_id)
        text = content['text']
        words = re.split('\W+',text)
        
        frequencies = {}
        for word in words[:1000]:
            word = stemmer.stem(word.lower())
            if len(word) > 3 and word not in stopwords:
                old_count = frequencies.get(word, 0)
                frequencies[word] = old_count + 1
        
        most_frequent = nlargest(10, frequencies.iteritems(), itemgetter(1))
        related_words = [ word[0] for word in most_frequent ]
        return related_words
    else:
        return []