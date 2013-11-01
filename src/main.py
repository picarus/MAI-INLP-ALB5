'''
Created on Oct 4, 2013

@author: Jose
'''


from url2text import clean, getFile

from namedEntity import processNE, initText

from tokenizer import tokenize_words, tokenize_sentences
from tagger import tag_words, tag_sentences
from tree2json import pprint_json_tree
import os
import codecs

# from stopwordcleaner import clear
from lemm_test import lemmstem

import json def process_files(rootpath):
    newpath = os.path.join(rootpath, 'processed_json')
    newpath = os.path.join(newpath, '')
    if not os.path.exists(newpath): os.makedirs(newpath)
    
    path = os.path.join(rootpath, 'original')
    path = os.path.join(path,'')
    
    files = os.listdir(path)
    for filename in files:
        print 'Processing', filename + '...'
        try:
            #f = codecs.open(path + filename, 'r', 'utf-8')
            f = open(path + filename, 'r')
            #data = f.read().encode('utf-8');
            data = f.read();
            f.close()
            text = clean(data); # return text without html
            #print(text)
            
            ## Using test text
            #text = initText();    
            
            # preprocessing
            
            # tokenize: Dani & Gerard
            tokenized = tokenize_sentences(text)
            # tagging: Dani & Gerard
            tagged= tag_sentences(tokenized)
            
            # named entities: Jose
            sentences = processNE(tagged)
            
            # lemmarization + stemming: Daniel Horowitz
            
            sentences = lemmstem(sentences)
            
            #print sentences
            
            s=pprint_json_tree(sentences)
            
            newfilename = 'processed_' + filename[9:-5] + '.json'
            f = codecs.open(newpath + newfilename, 'w', 'utf-8')
            f.write(s)
            f.close()
            
            #print s
            
        except Exception as exc:
            errfile = open('error.txt', 'a')
            errfile.write(filename + ' has the error: ' + str(type(exc))[18:-2] + ': ' + str(exc) + '\r\n')
            errfile.close()

if __name__ == '__main__':    
    
    ### iterate the src
    
    #url = 'http://en.wikipedia.org/wiki/Mick_Jagger'
    #data = getFile(url);
    
    PATH = "NonBio"
    PATH = "C:\Users\juan jose\Desktop\INLPTEST"
    process_files(PATH)
    #PATH = "Bio"
    #process_files(PATH)
