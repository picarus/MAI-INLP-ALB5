
'''
Created on Oct 10, 2013

@author: Jose
'''

import nltk

def initText():

    tt=u''' Peter lived in San Francisco.
    Michael enjoyed the travel to Almer\u00eda.
    Michael enjoyed the travel to Almeria.
    Daniel is a writer.
    John was born in Los Angeles.
    His wife met him in Costa Rica.
    Both studied at Stanford University.
    '''
    
    return tt

def processNE(sentences):
    
    sentences = [ nltk.ne_chunk(sent) for sent in sentences]
    
    return sentences