from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer

from wikipedia import get_related_wikipedia_words

def get_related_words(word):
    """
    Returns a list of stems related to the given word. 
    This includes synonyms, hypernyms, holonyms and antonyms of the word.
    """
    MAX_MEANINGS = 3
    MAX_LEMMAS = 2
    related_words = [word]
    
    # Iterate meanings
    syns = wn.synsets( word )
    
    for syn_index in range(min(MAX_MEANINGS,len(syns))):
        syn = syns[syn_index]
        
        # Synonyms
        related_words.extend(syn.lemma_names)
        
        # Hypernyms
        hypernyms = [ w.lemmas[0].name for w in syn.hypernyms()][:3]
        related_words.extend( hypernyms )
        print hypernyms
        
        # Holonyms
        member_holonyms = [ w.lemmas[0].name for w in syn.member_holonyms()][:3]
        related_words.extend( member_holonyms )
        print member_holonyms
        
        # Antonyms
        for lemma_index in range(min(MAX_LEMMAS,len(syn.lemmas))):
            antonyms = [ w.name for w in syn.lemmas[lemma_index].antonyms()][:3]
            related_words.extend( antonyms )

    
    group_words = [word.lower() for w in related_words if '_' in word]
    related_words = [word.lower() for w in related_words if not '_' in word]
    
    for w in group_words:
        related_words.extend(w.split('_'))
        
    # Stemming
    stemmer = PorterStemmer()
    related_words = [ stemmer.stem( w ) for w in related_words]
    
    # Wikipedia
    wikipedia_words = get_related_wikipedia_words(word)
    related_words.extend(wikipedia_words)
    print wikipedia_words
            
    related_words = list(set(related_words)) # Remove duplicates
        
    return related_words

if __name__ == "__main__":
    print get_related_words('kind')
