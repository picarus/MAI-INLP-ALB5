
from nltk import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet


lmtzr = WordNetLemmatizer()
st = LancasterStemmer()

dict = {'VB' :wordnet.VERB,
        'NN': wordnet.NOUN,
        'JJ':wordnet.ADJ,
        'RB':wordnet.ADV }

def lemmstem(sentences):
    
    for sent in sentences:
      
        nlvs=len(sent.leaves())
       
        for idx in xrange(0,nlvs):
            pos=sent.leaf_treeposition(idx)
            word=sent[pos][0]
            tag = sent[pos][1]
            rtag = tag[0:2]
            if rtag in dict:
                lemm=lmtzr.lemmatize( word, dict[rtag] )
                stem=st.stem(lemm)
                print word, lemm, stem
                sent[pos]=(word, tag, stem)
            else:
                sent[pos]=(word, tag, word)
    
    return sentences

# ORIGINAL CODE
#
# b = "write wrote writting writes written writer writers overwrite"
# lemm = []
# sentences = b.split(' ');
#
#     for x in range(0,len(words)):
#         print (lmtzr.lemmatize(words[x], wordnet.VERB))
#         lemm.append(lmtzr.lemmatize(words[x], wordnet.VERB))
#         
#     for x in range(0,len(lemm)):
#         print (st.stem(lemm[x]))
