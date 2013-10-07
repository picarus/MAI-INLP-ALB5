'''
Modified on 07/10/2013
Created on 07/10/2013

@author: Gerard Canal
@author: Dani Padilla
'''

import re
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize


def tokenize(text):
    ## Substitute  'ABC.DEF' by 'ABC. DEF' so the sentence
    ## tokenizer can split the sentences.
    text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
    
    #sentences = sent_tokenize(text)    
    #tokenized = [word_tokenize(sentence) for sentence in sentences]
    
    tokenized = word_tokenize(text)
    print [word for word in tokenized]
    
    return tokenized;