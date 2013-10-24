'''
Created on Oct 10, 2013

@author: Jose
'''

import nltk

def initText():
    tt=''' Peter lived in San Francisco.
    Daniel is a writer
    John was born in Los Angeles.
    His wife met him in Costa Rica.
    Both studied at University of Stanford.
    '''
    
    return tt

def processNE(sentences):
    
    sentences = [ nltk.ne_chunk(sent) for sent in sentences]
    
    return sentences