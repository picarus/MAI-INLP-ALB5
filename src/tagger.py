'''
Modified on 07/10/2013
Created on 07/10/2013

@author: Gerard Canal
@author: Dani Padilla
'''

from nltk.corpus import brown
from nltk.tag import UnigramTagger

def tag_words(word_list):
    
    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
    
    tagged_words = tagger.tag(word_list)
    
    print tagged_words 
    
    return tagged_words;