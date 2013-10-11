'''
Modified on 07/10/2013
Created on 07/10/2013

@author: Gerard Canal
@author: Dani Padilla
'''

import re
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize


def tokenize_words(text):
    ## Substitute  'ABC.DEF' by 'ABC. DEF' so the sentence
    ## tokenizer can split the sentences.
    #text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
    
    ## Tokenize results in an array of words
    tokenized = word_tokenize(text)
    
    return tokenized;

def tokenize_sentences(text):
    ## Substitute  'ABC.DEF' by 'ABC. DEF' so the sentence
    ## tokenizer can split the sentences.
    #text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
    
    ## Tokenize results in an array of 'sentences' (array of words)
    sentences = sent_tokenize(text)    
    tokenized = [word_tokenize(sentence) for sentence in sentences]
    
    return tokenized;