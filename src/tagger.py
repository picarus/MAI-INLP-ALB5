'''
Modified on 07/10/2013
Created on 07/10/2013

@author: Gerard Canal
@author: Dani Padilla
'''

import nltk
from nltk.corpus import brown
from nltk.tag import UnigramTagger

def tag_words(word_list):    
    ## Unigram Tagger is used to try different corpus
    ## If it goes wrong, comment this part and use pos_tag function
    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])    
    tagged_words = tagger.tag(word_list)
    
    ## pos_tag is generalized Tagger for NLTK 
    #tagged_words = nltk.pos_tag(word_list)
        
    return tagged_words;

def tag_sentences(sentences_list):    
    ## Unigram Tagger is used to try different corpus
    ## If it goes wrong, comment this part and use pos_tag function
    tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])    
    #tagged_words = [tagger.tag(s) for s in sentences_list]
    
    ## pos_tag is generalized Tagger for NLTK 
    tagged_sentences = [nltk.pos_tag(s) for s in sentences_list]
    
    return tagged_sentences;