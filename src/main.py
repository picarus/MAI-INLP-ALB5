'''
Created on Oct 4, 2013

@author: Jose
'''

from url2text import cleanHTML, cleanWIKI
from namedEntity import processNE   
from tokenizer import tokenize_sentences
from tagger import tag_sentences
from tree2json import pprint_json_tree
from lemm_test import lemmstem
import os
import codecs

####### API STARTS HERE

def preprocessText(textInput):
    """
    The method takes a complete text and performs a whole processing of it:
        Tokenizing
        Tagging
        Named Entities extraction
        Lemmarization and Stemization
    
    The text should not contain any markup (HTML, Wiki, XML, ... ) but just raw text.
    
    The result is a sequence of NLTK Tree structures (one for each sentence in the text).
    Named Entities correspond to the intermediate nodes of the tree
    The leaves are tuples of 3 elements: original word, part of speech, stem.
    """
    
    # preprocessing   
    # tokenize: Dani & Gerard
    tokenized = tokenize_sentences(textInput)
    # tagging: Dani & Gerard
    tagged= tag_sentences(tokenized)
    # named entities: Jose
    sentences = processNE(tagged)
    # lemmarization + stemming: Daniel Horowitz
    sentences = lemmstem(sentences)
    return sentences

def preprocessHTMLText(textStringInput):
    """
    Takes as input the contents of an HTML file and removes all HTML tags preserving the textual information.
    Applies the preprocessing returning the output of the preprocessText method.
    """
    text = cleanHTML(textStringInput)
    sentencesOutput = preprocessText(text)
    return sentencesOutput

def preprocessWIKIText(textStringInput):
    """
    Takes as input the contents of a WIKI file and removes all wikimedia format preserving the textual information.
    Applies the preprocessing returning the output of the preprocessText method.
    """
    text = cleanWIKI(textStringInput)
    sentencesOutput = preprocessText(text)
    return sentencesOutput

def preprocessHTML(fileinput):
    """
    Takes as input a path to an HTML file, loads the file and removes the HTML tags.
    Applies the preprocessing returning the output of the preprocessText method.
    """
    textStringInput=readFile(fileinput)
    sentencesOutput=preprocessHTMLText(textStringInput)
    return sentencesOutput

def preprocessWIKI(fileinput):
    """
    Takes as input a path to a WIKI file, loads the file and removes the WIKImedia tags.
    Applies the preprocessing returning the output of the preprocessText method.
    """
    textStringInput=readFile(fileinput)
    sentencesOutput=preprocessHTMLText(textStringInput)
    return sentencesOutput

def preprocessHTMLFile(fileinput, fileoutput):
    """
    Takes as parameter a path to an HTML file and after cleaning the HTML tags, preprocess the contents.
    The output is converted to JSON format and saved to the second file provided as parameter.
    """
    sentencesOutput=preprocessHTML(fileinput)
    writeFile(fileoutput,sentencesOutput)
    return
    
def preprocessWIKIFile(fileinput, fileoutput):
    """
    Takes as parameter a path to a WIKI file and after cleaning the WIKI tags, preprocess the contents.
    The output is converted to JSON format and saved to the second file provided as parameter.
    """
    sentencesOutput=preprocessWIKI(fileinput)
    writeFile(fileoutput,sentencesOutput)
    return

####### API FINISHES HERE

def readFile(filename):
    """ 
    Loads the specified file and returns its content.
    The file should not be binary.
    """
    
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data

def writeFile(filename, sentencesOutput):
    """
    Converts the NLTK tree structure in sentencesOutput to JSON format.
    The JSON object is saved to the file specified by filename.
    """
    s=pprint_json_tree(sentencesOutput)
    f = codecs.open(filename, 'w', 'utf-8')
    f.write(s)
    f.close()
    return

def process_files(rootpath):
    newpath = os.path.join(rootpath, 'processed_json')
    newpath = os.path.join(newpath, '')
    if not os.path.exists(newpath): os.makedirs(newpath)
    
    path = os.path.join(rootpath, 'original')
    path = os.path.join(path,'')
    
    files = os.listdir(path)
    for filename in files:
        print 'Processing', filename + '...'
        try:  
            newfilename = 'processed_' + filename[9:-5] + '.json'            
            preprocessHTMLFile(path + filename ,newpath + newfilename)
        except Exception as exc:
            errfile = open('error.txt', 'a')
            error = filename + ' has the error: ' + str(type(exc))[18:-2] + ': ' + str(exc) + '\r\n'
            errfile.write(error)
            errfile.close()
            print(error)

if __name__ == '__main__':    
    
    ### iterate the src
    
    #url = 'http://en.wikipedia.org/wiki/Mick_Jagger'
    #data = getFile(url);
        
    PATH = "NonBio"
    #PATH = "C:\Users\Dani\Desktop\NonBio"
    process_files(PATH)
    #PATH = "Bio"
    #process_files(PATH)
