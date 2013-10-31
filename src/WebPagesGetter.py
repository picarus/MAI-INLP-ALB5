from DBLinksGetter import get_links_gen
from url2text import getFile
import os
'''
Created on Oct 31, 2013

@author: danielhorowitz
'''
from locale import str
ORIGINAL = 'original'
CLEANED = 'cleaned'

def getWebPages():
    newpath = 'Bio'
     
    if not os.path.exists(newpath): os.makedirs(newpath)
    newpath = os.path.join(newpath,ORIGINAL)
    if not os.path.exists(newpath): os.makedirs(newpath)
    for id,url in get_links_gen(allCntnt=False,bio=True):
        print "fetching(Bio)" , url
        f = open(os.path.join(newpath,ORIGINAL + "_" + id),'w')
        f.write(getFile(url))
        
        
    newpath = 'NonBio'     
    if not os.path.exists(newpath): os.makedirs(newpath)
    newpath = os.path.join(newpath,ORIGINAL)
    if not os.path.exists(newpath): os.makedirs(newpath)
    for id,url in get_links_gen(allCntnt=False,bio=False):
        print "fetching(NonBio)" , url
        f = open(os.path.join(newpath,ORIGINAL + "_" + id),'w')
        f.write(getFile(url))
        
        
    if __name__=='__main__':
        getWebPages()