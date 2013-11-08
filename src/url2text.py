import urllib2
from bs4 import BeautifulSoup, NavigableString,Comment,Doctype

import codecs
###inFile = open('Dancers_urls.txt', 'r')

def getFile(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}
    
    request = urllib2.Request(url,None,headers) #The assembled request
    response = urllib2.urlopen(request)
    data = response.read() # The data u need
    response.close()
    return data;

def doctype(soup):
    items = [item for item in soup.contents if isinstance(item, Doctype)]
    return items[0] if items else None

def cleanWIKI(data):
    ''' your code here'''
    return None

def cleanHTML(data):
    
    # HTML A TEXT
    soup = BeautifulSoup(data)
    d = doctype(soup)
    if d != None :
        d.extract()
    [s.extract() for s in soup.findAll(['head', 'script'])]
    
#     a = [unicode(item) for item in soup];
#     f1 = codecs.open('C:\Users\Dani\Desktop\NonBio\clean.txt', 'w', 'utf-8')
#     f1.write(unicode("".join(a)))
#     f1.close()
    text = strip_tags(soup,'')
     
    return unicode(text)

def strip_tags(soup, invalid_tags):
    
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
