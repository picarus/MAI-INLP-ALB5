'''
Created on Oct 4, 2013

@author: Jose
'''


from url2text import clean, getFile

if __name__ == '__main__':
    
    ### iterate the src
    url = 'http://en.wikipedia.org/wiki/Mick_Jagger'
    data = getFile(url);
    text = clean(data); # return text without html
    print(text)
    # preprocessing
    # tokenize: Dani & Gerard
    # tagging: Dani & Gerard
    # stopwords: Dani & Gerard
    # stemming: Daniel Horowitz
    # named entities: Jose
    
    pass