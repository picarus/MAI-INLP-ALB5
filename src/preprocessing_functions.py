import MySQLdb
import os
import urllib2
import nltk
from nltk                import Tree, WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus         import wordnet
from nltk.tokenize       import word_tokenize, sent_tokenize
from locale              import str
from bs4                 import BeautifulSoup, NavigableString,Comment,Doctype
from wiki2plain          import Wiki2Plain
#from nltk.compat        import string_types, unicode_repr

#Constants
ORIGINAL = 'original'
CLEANED = 'cleaned'
INDENT_STEP = 2

#DBLinksGetter
def init():
    db_user = 'root'
    db_password = 'root'
    db = 'inlp'
    
    connection = MySQLdb.connect(host="localhost",user=db_user, passwd=db_password,db=db)
    return connection

def access_db(allCntnt=True,bio=True):
    #Get all the bio or non-bio links generator function
    connection = init()
    cur = connection.cursor()
    sql = "SELECT link FROM article"
    if not allCntnt:
        sql=sql+" WHERE is_bio = %s;" % (1 if bio else 0) # FIXME what about is_bio = -1?
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def get_links(allCntnt=True,bio=True):
    rows = access_db(allCntnt,bio)
    return [row[0].strip() for row in rows]

def get_links_gen(allCntnt=True, bio=True):
    rows = access_db(allCntnt,bio)
    for row in rows:
        yield row[0].strip()

#=====================================================================================
#WebPageGetter

def getWebPages():
    newpath = 'NonBio'
    getWebPagesType(newpath, False,dbid=11965) 
    newpath = 'Bio' 
    getWebPagesType(newpath, True,dbid=0)
        
def getWebPagesType(newpath,bio,dbid=0):        
         
    if not os.path.exists(newpath): os.makedirs(newpath)
    newpath = os.path.join(newpath,ORIGINAL)
    if not os.path.exists(newpath): os.makedirs(newpath)
    for myid,url in get_links_gen(allCntnt=False,bio=bio,dbid=dbid):
        try:
            print "fetching(%s)" % newpath , myid, url
            f = open(os.path.join(newpath,ORIGINAL + "_" + str(myid)) + '.html','w')
            text = getFile(url)
            f.write(text)    
        except Exception as exc:
            mystr = '%d,%s, %s \r\n' % (myid, url,str(exc))
            print mystr
            fe = open('errors.txt','a')
            fe.write(mystr)
            fe.close()
        finally:
            if f<>0:
                f.close()

#=====================================================================================
#url2text

def getFile(url):
    ''' This function download a file from a specified url and returns an HTML string.
        Input: String (url address) 
        Output: HTML text
    '''
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}
    
    request = urllib2.Request(url,None,headers) #The assembled request
    response = urllib2.urlopen(request)
    data = response.read() # The data u need
    response.close()
    return data;

def doctype(soup):
    ''' Search for the <!DOCTYPE html> tag and returns it
        Input: HTML text
        Output: DOCTYPE tag found
    '''
    
    items = [item for item in soup.contents if isinstance(item, Doctype)]
    return items[0] if items else None

def cleanWIKI(data):
    ''' Clean Wiki documents to get rid of markups and tags.
        Input: Wiki text
        Output: Clean text document
    '''
    
    wiki2plain = Wiki2Plain(data)
    text = wiki2plain.text
    
    return text # FIXME returning data to test!

def cleanHTML(data):
    ''' This function is the responsible of removing the 
        tags from a HTML it returns a string of the 
        processed HTML. 
        Input: HTML file in a string format 
        Output: string with the HTML tags removed
    '''
    # HTML to TEXT
    soup = BeautifulSoup(data)
    d = doctype(soup)
    if d != None :
        d.extract()
    [s.extract() for s in soup.findAll(['head', 'script'])]
    
    text = strip_tags(soup,'')
     
    return unicode(text)

def strip_tags(soup, invalid_tags):
    ''' This function removes any HTML tag from a string. 
        Input:  NavigableString (soup) 
        Output: NavigableString (soup) without HTML tags.
    '''
    s = soup.string
    if s != None and not (isinstance(s, Comment)):
        return NavigableString(s)
    elif (isinstance(s, Comment)) or (len(soup.contents)==0):
        return NavigableString('')
    else:
        tags = soup.children
        newstring = ''
        for tag in tags:
            newstring += unicode(strip_tags(tag,''))
        soup = NavigableString(newstring)
    return soup

#=====================================================================================
#tokenizer

def tokenize_sentences(text):
    ''' Make a tokenization (spliting) of the sentences of a text
        followed by a tokenization of this sentences for tekenizing the words.
        Input:  Clean text document
        Output: Lists of list of String consisting of a List of sentences where
                every sentence is a list of words.
    '''
    
    ## Tokenize results in an array of 'sentences' (array of words)
    sentences = sent_tokenize(text)    
    tokenized = [word_tokenize(sentence) for sentence in sentences]
    
    return tokenized;

#=====================================================================================
#tagger

def tag_sentences(sentences_list):    
    ''' Using nltk.pos_tag() we are tagging words using the corpus Maximum
        Entropy Treebank POS tagger.
        Input:  Text splitted by sentences
        Output: Structure of trees (Each sentences has its own words with its tags)
    '''
    
    ## pos_tag is generalized Tagger for NLTK 
    tagged_sentences = [nltk.pos_tag(s) for s in sentences_list]
    
    return tagged_sentences;

#=====================================================================================
#Named Entity

def processNE(sentences):
    """ 
        Takes the list of sentences where each sentence has been tagged and
        makes the Named Entity recognition using default NLTK method.
        Input: List of sentences where each sentence is a list of POS tagged words
        Output: Each of the sentence will be an NLTK tree where each intermediate node
                is a Named Entity that includes the child nodes as elements of the Named Entity 
    """
        
    sentences = [ nltk.ne_chunk(sent) for sent in sentences]
    
    return sentences

#=====================================================================================
#Lemmarization & Stemming

def lemmstem(sentences):
    ''' This function is responsible for perfoming 
        the lemmarization and stemming of the words
        Input: A list of trees containing the sentences.
                All words are classificated by their NE type
        Output: Lemmatized/Stemmized sentences
    '''
    
    lmtzr = WordNetLemmatizer()
    st = LancasterStemmer()
    
    dic = {'VB' :wordnet.VERB,
            'NN': wordnet.NOUN,
            'JJ':wordnet.ADJ,
            'RB':wordnet.ADV }
    
    for sent in sentences:
      
        lvsidx=sent.treepositions('leaves') 
       
        for pos in lvsidx:
            word=sent[pos][0]
            tag = sent[pos][1]
            rtag = tag[0:2]
            if rtag in dic:
                lemm=lmtzr.lemmatize( word, dic[rtag] )
                stem=st.stem(lemm)
                #print word, lemm, stem #Linia maldita
                sent[pos]=(word, tag, stem)
            else:
                sent[pos]=(word, tag, word)
    
    return sentences

#=====================================================================================
#tree2jason

def pprint_json_tree(sentences):
        """
        Returns a representation of the list of trees in JSON format.
        Each sentence in the text will be a tree. And each sentence itself can contain other trees.

        For example, the following result was generated from a parse tree of
        the sentence ``Peter lived in San Francisco.``::
        
        [ Tree('S', [Tree('PERSON', [('Peter', 'NNP', 'pet')]), ('lived', 'VBD', 'liv'), ('in', 'IN', 'in'), Tree('GPE', [('San', 'NNP', 'san'), ('Francisco', 'NNP', 'francisco')]), ('.', '.', '.')])
        
        (S
          (PERSON Peter/NNP/pet)
          lived/VBD/liv
          in/IN/in
          (GPE San/NNP/san Francisco/NNP/francisco)
          ././.)

        {
            tag:'S',
            content:
            [
                {   
                    tag:'PERSON',
                    content: 
                    [
                        ['Peter', 'NNP', 'pet']
                    ]
                },
                ['lived', 'VBD', 'liv'], 
                ['in', 'IN', 'in'],
                {
                    tag:'GPE',
                    content: 
                    [   
                        ['San', 'NNP', 'san'], 
                        ['Francisco', 'NNP', 'francisco']
                    ]
                },
                ['.', '.', '.']
            ]
        }

        :return: A JSON representation of this tree.
        :rtype: str
        """

        text='['
        #reserved_chars = re.compile('"\/') # review !!!!
        first = True
        for sentence in sentences:
            output = pprint(sentence, True, 0)
            if not first:
                text = text + ','
            text = text + output #re.sub(reserved_chars, r'\\\1', output)
            first = False
        text = text + ']'

        return text
    
    
def pprint(element, first, indent, nodesep='', quotes=False):
    """
    :return: A pretty-printed string representation of this tree.
    :rtype: str
    :param margin: The right margin at which to do line-wrapping.
    :type margin: int
    :param indent: The indentation level at which printing
        begins.  This number is used to decide how far to indent
        subsequent lines.
    :type indent: int
    :param nodesep: A string that is used to separate the node
        from the children.  E.g., the default value ``':'`` gives
        trees like ``(S: (NP: I) (VP: (V: saw) (NP: it)))``.
    """

    # write it on multi-lines.
    s = ''
    if not first:
        s += ','   # a comma may be missing if it is not the first child
    if isinstance(element, Tree):                      
        s += '\n'+' '*(indent)+'{'
        indent += INDENT_STEP
        s += '\n'+' '*(indent)+"tag:'"+element.node+"',"
        s += '\n'+' '*(indent)+'content:'
        s += '\n'+' '*(indent)+'[' 
        for idx in xrange(0,len(element)):
            s += pprint(element[idx], idx==0, indent+INDENT_STEP, nodesep, quotes)
        s += '\n'+' '*(indent)+']'
        indent -= INDENT_STEP 
        s+= '\n'+' '*(indent)+'}'     
    elif isinstance(element, tuple):
        s += '\n'+' '*(indent)+"['"+ "','".join([ elem for elem in element])+"']"
    else:
        s=str(element)
            
    return s

