'''
Modified on 07/10/2013
Created on 07/10/2013

@author: Gerard Canal
@author: Dani Padilla
'''

from nltk.corpus import stopwords

def clear(text):
    
    ## Get the generic stopword list
    stopwordlist = stopwords.words('english')
    
    ## Remove stopfords from text
    content = [w for w in text if w.lower() not in stopwordlist]
    
    return content;