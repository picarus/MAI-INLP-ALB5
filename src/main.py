
from preprocessing_functions import cleanHTML, cleanWIKI, processNE, tokenize_sentences
from preprocessing_functions import tag_sentences, pprint_json_tree, lemmstem
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

def preprocessHTML(fileinput, codec='utf-8'):
    """
    Takes as input a path to an HTML file, loads the file and removes the HTML tags.
    Applies the preprocessing returning the output of the preprocessText method.
    The codec for the file can be specified. The default is 'utf-8'.
    On windows files the codec 'utf-8-sig' should be used instead.
    """
    textStringInput=readFile(fileinput, codec)
    sentencesOutput=preprocessHTMLText(textStringInput)
    return sentencesOutput

def preprocessWIKI(fileinput, codec='utf-8'):
    """
    Takes as input a path to a WIKI file, loads the file and removes the WIKImedia tags.
    Applies the preprocessing returning the output of the preprocessText method.
    The codec for the file can be specified. The default is 'utf-8'.
    On windows files the codec 'utf-8-sig' should be used instead.
    """
    textStringInput=readFile(fileinput, codec)
    sentencesOutput=preprocessWIKIText(textStringInput)
    return sentencesOutput

def preprocessHTMLFile(fileinput, fileoutput, codec='utf-8'):
    """
    Takes as parameter a path to an HTML file and after cleaning the HTML tags, preprocess the contents.
    The output is converted to JSON format and saved to the second file provided as parameter.
    The codec for the file can be specified. The default is 'utf-8'.
    On windows files the codec 'utf-8-sig' should be used instead.
    """
    sentencesOutput=preprocessHTML(fileinput, codec)
    writeFile(fileoutput,sentencesOutput, codec)
    return
    
def preprocessWIKIFile(fileinput, fileoutput, codec='utf-8'):
    """
    Takes as parameter a path to a WIKI file and after cleaning the WIKI tags, preprocess the contents.
    The output is converted to JSON format and saved to the second file provided as parameter.
    The codec for the file can be specified. The default is 'utf-8'.
    On windows files the codec 'utf-8-sig' should be used instead.
    """
    sentencesOutput=preprocessWIKI(fileinput, codec)
    writeFile(fileoutput,sentencesOutput, codec)
    return

####### API FINISHES HERE

def processTextFiles(path, codec='utf-8'):
    """
    For the given path folder, takes all the files on it and tries to clean them.
    The files are supposed to be text files.
    The output will be stored in a subfolder called 'clean'.
    The codec for the files can be specified. The default is 'utf-8'.
    On windows files the codec 'utf-8-sig' should be used instead.
    """    
    files = os.listdir(path)
    newpath = os.path.join(path, 'clean')
    if not os.path.exists(newpath): os.makedirs(newpath)
    
    for filename in files:
        print 'Processing', filename + '...'
        try:  
            newfilename = filename+ '.json'            
            preprocessTextFile(os.path.join(path, filename) ,os.path.join(newpath, newfilename), codec)
        except Exception as exc:
            errfile = open('error.txt', 'a')
            error = filename + ' has the error: ' + str(type(exc))[18:-2] + ': ' + str(exc) + '\r\n'
            errfile.write(error)
            errfile.close()
            print(error)
                
    return


def processWIKIFiles(path, codec='utf-8'):
    """
    Processes all the files assuming that they are from Wikipedia with wikimedia tags.
    The path is assumed to be the root of a folder that contains a subfolder "occupaions"
    which has inside a folder for every possible occupation, and inside that folder a folder called "docs"
    with all the wiki files.
    """
    newpath = os.path.join(path, 'clean')
    if not os.path.exists(newpath): os.makedirs(newpath)
    path = os.path.join(path, 'occupations')
    occupations = os.listdir(path)
    for occupation in occupations:
        occupation_path = os.path.join(path, os.path.join(occupation, 'docs'))
        files = os.listdir(occupation_path)
        if 'index.txt' in files:
            files.remove('index.txt')
        for filename in files:
            print 'Processing', occupation +'/'+filename + '...'
            try:  
                newfilename = filename + '.json'
                new_occupation_path = os.path.join(newpath, occupation)
                if not os.path.exists(new_occupation_path): os.makedirs(new_occupation_path)
                preprocessWIKIFile(os.path.join(occupation_path, filename), os.path.join(new_occupation_path, newfilename), codec)
            except Exception as exc:
                errfile = open('error.txt', 'a')
                error = filename + ' has the error: ' + str(type(exc))[18:-2] + ': ' + str(exc) + '\r\n'
                errfile.write(error)
                errfile.close()
                print(error)
            
def preprocessTextFile(fileInput, fileOutput, codec='utf-8'):

    """
    Process a clean text file and generates the corresponding JSON file as output
    """
    textStringInput=readFile(fileInput, codec)
    sentencesOutput=preprocessText(textStringInput)
    #print sentencesOutput
    writeFile(fileOutput,sentencesOutput)
    return

def readFile(filename, codec='utf-8'):
    """ 
    Loads the specified file and returns its content.
    The file should not be binary.
    """
       
    f = codecs.open(filename, 'r', codec)
    data = f.read()
    f.close()
    return data

def writeFile(filename, sentencesOutput, codec='utf-8'):
    """
    Converts the NLTK tree structure in sentencesOutput to JSON format.
    The JSON object is saved to the file specified by filename.
    """
    s=pprint_json_tree(sentencesOutput)
    f = codecs.open(filename, 'w', codec)
    f.write(s)
    f.close()
    return

def processHTMLfiles(rootpath, codec='utf-8'):
    """
    Processes all the files in the rootpath folder. It assumes that all the files are together in
    a folder called 'original' inside the rootpath. Then it creates the folder 'processed_json' with 
    the results inside.
    """
    newpath = os.path.join(rootpath, 'processed_json')
    newpath = os.path.join(newpath, '')
    if not os.path.exists(newpath): os.makedirs(newpath)
    
    path = os.path.join(rootpath, 'original')
    path = os.path.join(path,'')
    
    files = os.listdir(path)
    for filename in files:
        print 'Processing', filename + '...'
        try:  
            newfilename = 'processed_' + filename[:-5] + '.json'            
            preprocessHTMLFile(path + filename ,newpath + newfilename, codec)
        except Exception as exc:
            errfile = open('error.txt', 'a')
            error = filename + ' has the error: ' + str(type(exc))[18:-2] + ': ' + str(exc) + '\r\n'
            errfile.write(error)
            errfile.close()
            print(error)

if __name__ == '__main__':

#    processTextFiles('dataset','utf-8-sig')  # for windows the codec should be 'utf-8-sig' instead of 'utf-8'
        
    NonBioPATH = "dataset\\NonBio"
    processHTMLfiles(NonBioPATH)
    BioPATH = "dataset\\Bio"
    processWIKIFiles(BioPATH)
