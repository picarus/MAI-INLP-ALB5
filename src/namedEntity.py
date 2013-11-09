
'''
Created on Oct 10, 2013
@author: Jose
'''

import nltk

def initText():
    """ 
    Initializes a simple text to be used for testing the processing part of the module.
    A list of sentences with different Name Entity types, reqular and irregular verbs and some unicode characters are included.
    """

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
    """ 
    Takes a list of sentences stored in an NLTK Tree structure and does Name Entity Recognition generating intermediate nodes
    with the Named Entity discovered. The sentences must be tokenized and tagged prior to the NE recognition process.
    """
    
    sentences = [ nltk.ne_chunk(sent) for sent in sentences]
    
    return sentences