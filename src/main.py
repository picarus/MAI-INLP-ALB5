'''
Created on Oct 4, 2013

@author: Jose
'''


from url2text import clean, getFile
from tokenizer import tokenize
from tagger import tag_words
from stopwordcleaner import clear


if __name__ == '__main__':    
    
    ### iterate the src
    url = 'http://en.wikipedia.org/wiki/Mick_Jagger'
    data = getFile(url);
    text = clean(data); # return text without html
    print(text)
    # preprocessing
    
    # tokenize: Dani & Gerard
    tokenized = tokenize(text)
    # stopwords: Dani & Gerard
    cleartext = clear(tokenized)
    # tagging: Dani & Gerard
    tagged_words = tag_words(cleartext)
    # stemming: Daniel Horowitz
    # named entities: Jose
    
    pass