import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def word_feats(words):
    global stemmer
    return dict([(stemmer.stem(word), True) for word in words])


def treat_parts(parts):
    return [f.split("=")[1] for f in parts]

def read_corpus(path):
    words = []
    f = open(path)
    while(True):
        line = f.readline()
        if not line:
            return words
        parts = treat_parts(line.split(" "))
        
        #format: word, subjectivity, polarity
        word = (parts[2], parts[0], parts[5][:-1])
        words.append(word) 


our_corpus = read_corpus("corpus.tff")

negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')
    

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
negfeats.extend([(word_feats([f[0]]), 'neg') for f in our_corpus if f[2] == 'negative'])
 
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]
posfeats.extend([(word_feats([f[0]]), 'pos') for f in our_corpus if f[2] == 'positive'])

neutralfeats = [(word_feats(['']), 'neutral') for w in range(10000)]

trainfeats = posfeats + negfeats + neutralfeats

print len(posfeats), len(negfeats), len(neutralfeats)

polar_classifier = NaiveBayesClassifier.train(trainfeats)


def classify_words(words):
    global polar_classifier
    stats = {}
    stats['pos'] = 0
    stats['neg'] = 0
    stats['neutral'] = 0
    for word in words:
        classification = polar_classifier.classify(word_feats([word]))
        print (word, classification)
        stats[classification] += 1
    return stats


if (__name__ == "__main__"):
    stats = classify_words(['nailed','shit','drop','little', 'ability', 'death', 'fear', \
                             'courage', 'cool', 'unsuccessful', 'congratulations'])
    
    print stats['pos']
    print stats['neg']
