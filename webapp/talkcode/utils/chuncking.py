from nltk import pos_tag, word_tokenize, RegexpParser
import nltk.data

from django.conf import settings

tok = nltk.data.load('tokenizers/punkt/english.pickle')


def chunck_text(text):
    sentences = tok.tokenize(text)

#    phrases = []
#    for sentence in sentences:
#        phrases.extend(divide_phrases(sentence))
    
    return sentences

def divide_phrases(sentence):

    tokens = pos_tag(word_tokenize(sentence))

    connectors = []
    verbs = []
    for index, token in enumerate(tokens):
        if token[1] in ['CC',',',':']: # Seperators
            connectors.append(index)
        if token[1] in ['VB','VBD','VBZ','VBP','VBN']: # Verbal forms
            verbs.append(index)

    cursor = 0
    phrases = []

    if connectors and verbs:
        
        # Jump to the connector after the first verb
        connector_index = 0
        while (connector_index < len(connectors) and connectors[connector_index] < verbs[0]):
               connector_index += 1
    
        if connector_index != len(connectors):
        
            for verb_index in verbs[1:]:
                found = False
                while connector_index < len(connectors) and connectors[connector_index] < verb_index:
                    connector_index += 1
                    found = True
                if found:
                    phrases.append(tokens[cursor:connectors[connector_index-1]])
                    cursor = connectors[connector_index-1]

    phrases.append(tokens[cursor:]) # Add last phrase

    phrases = [' '.join([ token[0] for token in phrase ]) for phrase in phrases] # Join all tokens

    return phrases

if __name__ == "__main__":
    print chunck_text("At the end of World War I in 1918, the Weimar Republic was proclaimed in Berlin. In 1920, the Greater Berlin Act incorporated dozens of suburban cities, villages, and estates around Berlin into an expanded city. This new area encompassed Spandau and Charlottenberg in the west, as well as several other areas that are now major municipalities. After this expansion, Berlin had a population of around four million. During the Weimar era, Berlin became internationally renowned as a center of cultural transformation, at the heart of the Roaring Twenties.")

