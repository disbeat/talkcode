import nltk.classify.util
from nltk import pos_tag, word_tokenize, RegexpParser
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.stem.porter import PorterStemmer
from categorization import retrieve_relevant_words

anypos_list = ['c','d','e','f','i','j','l','m','n','p','r','s','t','u','v']

use_pos = False
use_subj = False
threashold = 2

def word_feats(word, pos):
    global stemmer, use_pos
    if not use_pos:
        pos = ''
    return dict( [(stemmer.stem(word.lower()), pos.lower())] )

def treat_parts(parts):
    return [f.split("=")[1] for f in parts]

def read_corpus(path):
    stats = dict([('neu', 0),('pos',0), ('neg',0), ('bot',0)])
    words = []
    f = open(path)
    while(True):
        line = f.readline()
        if not line:
            return words, stats
        parts = treat_parts(line.split(" "))

        #format: word, subjectivity, polarity, pos
        word = (parts[2], parts[0], parts[5][:3], parts[3])
        stats[word[2]] += 1
        words.append(word)


def prepare_training_feats_polarity(corpus):
    global use_pos
    train = []
    for word in corpus:
        if word[3] == 'anypos':
            train.extend([(word_feats(word[0], pos), word[2]) for pos in anypos_list])
        else:
            train.append((word_feats(word[0], word[3]), word[2]))
        
    for i in range(8000):
        train.extend([(word_feats('lixo', pos), 'neu') for pos in anypos_list])
        
    if not use_pos:
        print
        negids = movie_reviews.fileids('neg')
        posids = movie_reviews.fileids('pos')
        for id in negids:
            for word in movie_reviews.words(fileids=[id]):
                train.append((word_feats(word, ''),'neg'))
        for id in posids:
            for word in movie_reviews.words(fileids=[id]):
                train.append((word_feats(word, ''),'pos'))
    
    return train

def prepare_training_feats_subjectivity(corpus):
    train = []
    for word in corpus:
        if word[3] == 'anypos':
            train.extend([(word_feats(word[0], pos), word[1]) for pos in anypos_list])
        else:
            train.append((word_feats(word[0], word[3]), word[1]))
        
    for i in range(8000):
        train.extend([(word_feats('lixo', pos), 'neu') for pos in anypos_list])
    return train


stemmer = PorterStemmer()
(our_corpus, stats) = read_corpus("../../corpus.tff")

print stats

trainfeats_subjectivity = prepare_training_feats_subjectivity(our_corpus)
subjectivity_classifier = NaiveBayesClassifier.train(trainfeats_subjectivity)

trainfeats_polarity = prepare_training_feats_polarity(our_corpus)
polar_classifier = NaiveBayesClassifier.train(trainfeats_polarity)


def classify_words(words):
    global polar_classifier, subjectivity_classifier, use_subj
    
    scalor = dict([('neu', 1),('weaksubj',2), ('strongsubj',4)])
    stats = dict([('neu', 0),('pos',0), ('neg',0), ('bot',0)])
    
    for word in words:
        factor = 1
        if use_subj:
            subjectivity = subjectivity_classifier.classify(word_feats(word[0], word[1]))    
            factor = scalor[subjectivity]
        
        classification = polar_classifier.classify(word_feats(word[0], word[1]))
        stats[classification] += factor
        #print word, classification, subjectivity, factor
    return stats


def classify_phrase(phrase):
    global threashold
    tokens = pos_tag(word_tokenize(phrase))

    words = retrieve_relevant_words(phrase)
    to_classify = []
    
    tokens_list = [token for junk, token in enumerate(tokens)]
    
    index = 0
    for word in words:
        
        while(len(tokens_list) > 0):
            token = tokens_list.pop(0)
            if stemmer.stem(token[0]).lower() == word.lower():
                to_classify.append((word, token[1].lower()[0]))
                break

    stats = classify_words(to_classify)
    
    total_polar = stats['pos'] + stats['neg']
    if not total_polar:
        return 0
    
    pos_rate = stats['pos'] * 1.0 / total_polar
    neg_rate = stats['neg'] * 1.0 / total_polar
    
    #print phrase, pos_rate, neg_rate
    
    if pos_rate > neg_rate and (not neg_rate or pos_rate / neg_rate > threashold):
        return 1
    elif pos_rate < neg_rate and (not pos_rate or neg_rate / pos_rate > threashold):
        return -1
    else:
        return 0

if (__name__ == "__main__"):
    
    results = [[0,0,0],[0,0,0],[0,0,0]]
