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
        except Exception:
            mystr = '%d,%s, %s \r\n' % (myid, url, Exception.message)
            print mystr
            fe = open('errors.txt','a')
            fe.write(mystr)
            fe.close()
        finally:
            if f<>0:
                f.close()
        
              
if __name__ == '__main__':
    getWebPages()