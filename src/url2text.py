import urllib2
from bs4 import BeautifulSoup

inFile = open('Dancers_urls.txt', 'r')

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,}
text = ''

#url = inFile.readline()
url = 'http://www.technologyreview.com/view/419223/using-neural-networks-to-classify-music/'
request = urllib2.Request(url,None,headers) #The assembled request
response = urllib2.urlopen(request)
data = response.read() # The data u need
response.close()


# HTML A TEXT
soup = BeautifulSoup(data)
text_parts = soup.find_all('p')
i=0
string_list = []
for item in text_parts:
    i=i+1
    for string in item.stripped_strings:
        string_list.append(repr(string))

text = ''.join(string_list).replace("'",'')

print(text)
