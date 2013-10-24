'''
Created on Oct 4, 2013

@author: Jose
'''


from url2text import clean, getFile

from namedEntity import processNE, initText

from tokenizer import tokenize_words, tokenize_sentences
from tagger import tag_words, tag_sentences
# from stopwordcleaner import clear
from lemm_test import lemmstem
if __name__ == '__main__':    
    
    ### iterate the src
    
    url = 'http://en.wikipedia.org/wiki/Mick_Jagger'
    data = getFile(url);
    text = clean(data); # return text without html
    print(text)
    
    ## Using test text
    text = initText();    
    
    # preprocessing
    
    # tokenize: Dani & Gerard
    tokenized = tokenize_sentences(text)
    # tagging: Dani & Gerard
    tagged= tag_sentences(tokenized)
    
    # named entities: Jose
    sentences = processNE(tagged)
    
    # lemmarization + stemming: Daniel Horowitz
    
    sentences = lemmstem(sentences)
    
    print sentences
    
    # stopwords should be done as a final step: Dani & Gerard
    #cleartext = clear(sentences)
    
    pass