import lxml.html as lh
from types import *
import urllib2
from  urllib2 import urlopen
import logging
from datetime import date
from datetime import datetime
import csv


class htmlParser:
    def __init__(self , url , tagType):
        self.url = url
        self.tagType = tagType
        
    def removeNonAscii(self , text):

        return ''.join([i if ord(i) < 128 else ' ' for i in text]) 
    
    def fetchText(self):
        logging.debug(str(datetime.now()) + " ## START htmlParser ## " + self.url)
        
        text = ' '
        
        try:
            req = urllib2.Request(self.url, headers={'User-Agent' : "Magic Browser"})
            f = urlopen(req)
            #f = urlopen(self.url)
            html = f.read()
            #Returns document_fromstring or fragment_fromstring, based on whether the string looks like a full document, or just a fragment.
            root = lh.fromstring(html)
            #Select elements from this element and its children, using a CSS selector expression. (Note that .xpath(expr) is also available as on all lxml elements.)
            articleElements = root.cssselect(self.tagType)
            
            
        
            if len(articleElements) == 0:
                return text
            
       

#         # Strategy one, script and function data also comes while using this.
#             text = articleElements[0].text_content()
            
          
          
           
        #Strategy two, currently in use 
            nestedElements = articleElements[0].cssselect('*')
              
            for elem in nestedElements:
                if elem.tag not in ['script','style']:
                    if type(elem.text) in [StringType, UnicodeType]:
                         
                        text = text + elem.text.rstrip() + '. '
                         
#                            Checking length on every addition increases runtime by 8times on average.
#                         if( len(text_f) > 32767 ):
#                             break
#                         else:
#                             text=text_f
        
        except Exception as e:
            logging.warning( "Could not process article from " + str( self.url))
            return self.removeNonAscii(text)
            
        return self.removeNonAscii(text) 


# start =  datetime.now()
# obj = htmlParser('http://www.winbeta.org/news/classrooms-around-the-world-invited-to-participate-in-skype-a-thon', 'article')
# text = obj.fetchText()
# 
# with open("C:\Users\Jyoti.Gupta\Documents\crawler\sample.csv" , 'ab') as csvFile:
#             csvWriter = csv.writer(csvFile, delimiter="," , quoting=csv.QUOTE_ALL)
#             
#             csvWriter.writerow([ text[:32760]])
#             
# print (datetime.now()-start).total_seconds()