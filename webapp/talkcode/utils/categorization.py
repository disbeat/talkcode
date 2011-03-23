from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem.porter import PorterStemmer

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
sys.path.append('..')
sys.path.append('../..')

from takcode.models import *

TOPIC_FACTOR =      0.5
TOPIC_TERM_FACTOR = 0.3
SYNONYM_FACTOR =    0.1
THRESHOLD = 0.0

stemmer = PorterStemmer()

def categorize_phrase(phrase, entry):
    
    words = retrieve_relevant_words(phrase)
    topics = Topic.objects.filter(account = entry.account)
    
    scores = {}
    for topic in topics:
        scores[topic] = 0
    
    for word in words:
        score = categorize_word(word, topics)
        for topic in topics:
            scores[topic] += score[topic]
    
    scores_set = scores.items()
    scores_set.sort(key=lambda score: score[1], reverse=True)
    
    return (scores_set[0][1] > THRESHOLD and scores_set[0][0] or None) 

stopwords = nltk_stopwords.words('english')
irrelevant_words = ['...']
non_removing_words = ['not', 'no']

def retrieve_relevant_words(phrase):
    
    def is_relevant_word(word):
        return len(word) > 2 and \
               word not in stopwords and \
               word not in irrelevant_words or \
               word in non_removing_words
               
    
    import re
    splitter = re.compile(r'([, \:\.!\?"\(\)]|\.\.\.)')
    words = splitter.split(phrase)
    
    relevant_words = [ word for word in words if is_relevant_word(word) ]
    stemmed_words = stem_words( relevant_words )
    return stemmed_words


def stem_words(words):
    return [ stemmer.stem(word) for word in words ]


def categorize_word(word, topics):
    score = {}
    for topic in topics:
        score[topic] = categorize_topic(word, topic)
    return score


def categorize_topic(word, topic):
    
    total = categorize_term(word, topic.term) * TOPIC_FACTOR
    
    topic_terms = topic.auxiliary_terms.all()
    for topic_term in topic_terms:
        total += categorize_term(word, topic_term.term) * TOPIC_TERM_FACTOR * topic_term.relevance()
    
    return total
 

def categorize_term(word, term):
    
    if word == stemmer.stem(term.name): print 'Match:',word
    total = ( word == stemmer.stem(term.name) and 1 or 0 )
    
    synonyms = term.synonyms.all()
    for synonym in synonyms:
        total += categorize_synonym(word, synonym) * SYNONYM_FACTOR
    
    return total
 

def categorize_synonym(word, synonym):
    if word == synonym.word: print 'Match:',word
    return ( word == synonym.word and 1 or 0 )

 
if __name__ == "__main__":
    import sys
    from os import environ
    sys.path.append('..')
    sys.path.append('../..')
    environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    
    
    print retrieve_relevant_words("At. (the) \"end\"... of?? World War! I,, in 1918, the Weimar Republic was proclaimed in Berlin. In 1920, the Greater Berlin Act incorporated dozens of suburban cities, villages, and estates around Berlin into an expanded city. This new area encompassed Spandau and Charlottenberg in the west, as well as several other areas that are now major municipalities. After this expansion, Berlin had a population of around four million. During the Weimar era, Berlin became internationally renowned as a center of cultural transformation, at the heart of the Roaring Twenties.")

    