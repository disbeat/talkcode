'''
Created on 2010/11/12

@author: disbeat
'''

from nltk import pos_tag, word_tokenize, RegexpParser

key_words = ["function", "class", "to", "do", "comment", "method", "variable", "integer", "string", "double", "float", "constructor", "destructor", "create"]

def choose_best_phrase(matches):
	max = 0
	best = None
	for match in matches:
		
		words = word_tokenize(match)
		count = 0
		for word in words:
			if word in key_words:
				count += 1
		if count > max:
			max = count
			best = match
	return best


def divide_phrases(sentence):

    tokens = pos_tag(word_tokenize(sentence))

    print tokens
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

def process(text):
    phrases = divide_phrases(text)
    
    for phrase in phrases:
        print phrase
    
    
if __name__ == "__main__":
    process("create class person details with attributes name as string and age as integer")