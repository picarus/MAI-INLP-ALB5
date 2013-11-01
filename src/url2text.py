import urllib2
from bs4 import BeautifulSoup, NavigableString,Comment

###inFile = open('Dancers_urls.txt', 'r')

def getFile(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent':user_agent,}
    
    request = urllib2.Request(url,None,headers) #The assembled request
    response = urllib2.urlopen(request)
    data = response.read() # The data u need
    response.close()
    return data;

def clean(data):
    
    # HTML A TEXT
    soup = BeautifulSoup(data)
    [s.extract() for s in soup('script')]
    text = strip_tags(soup.body,'')
    
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
