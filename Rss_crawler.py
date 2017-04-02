import feedparser
import csv
import getopt
import sys
from _sqlite3 import Row
from datetime import date
from datetime import datetime

from fileinput import filename
from htmlParser import htmlParser
import pickle
import logging
import os.path
import re


import header
from time import mktime


class Crawler:
    
        
    def __init__(self):
        crawlerStartTime = datetime.now()
        logging.info( str(crawlerStartTime) + " ############## START CRAWLER #################################################")
        self.numOfMsgCrawled = 0
        if not os.path.exists(header.outputFilePath):
            with open(header.outputFilePath , 'ab') as csvFile:
                writer = csv.writer(csvFile, delimiter="," , quotechar='"', quoting=csv.QUOTE_ALL)
                writer.writerow(["ArticleTitle" , "Summary" , "Link" , "Timestamp" , "Category" , "Keyword" , "ArticleStory" ])
            
        self.keywordList = self.populateKeywordList()
        self.sites = self.populateSiteInformation()
        self.siteLastCrawled = self.populateSiteLastCrawled()
        self.processSites()
        crawlerEndTime = datetime.now()
        
        
        #TODO Divide by zero exception might occur here, Beware gal
       
        crawlerSpeed =   self.numOfMsgCrawled / ( crawlerEndTime - crawlerStartTime ).total_seconds()
            
        logging.info(str(datetime.now()) + " CRAWLER SPEED :: " + str(crawlerSpeed) + " articles/sec" )
        logging.info(str(datetime.now()) + " ############## END CRAWLER #################################################")
        
    
    def __del__(self):
        with open(header.siteTimestampPickleFile, "wb") as fp:
            pickle.dump(self.siteLastCrawled, fp)
   
    def populateSiteLastCrawled(self):
        
        try:
            with open(header.siteTimestampPickleFile) as fp:
                siteTimeStampInfo =  pickle.load(fp)
                return siteTimeStampInfo
        
        except Exception as e:
            # Create empty dictionary in case pickle file is not found.
            return dict()
        
          
    def populateKeywordList(self):
        keywordList = []
        
        with open(header.keywordFilePath , 'rt') as csvFile:
            try:
                reader = csv.reader(csvFile)
                for row in reader:
                    keywordList.append(row[0].lower())
                                                                                                  
            finally:
                csvFile.close()
            
        return keywordList
    
    # Parse Site Information file for which data is to be crawled.
    def populateSiteInformation(self):
        sites = []
        with open(header.siteInfoFilePath , 'rt') as csvFile:        
            try:
                reader = csv.reader(csvFile)
                for row in reader:
                    isActive = bool(row[1])
                    if (isActive):
                        sites.append(row[0])
                                                                                                  
            finally:
                csvFile.close()
        return sites
         
    
    def processSites(self):
        logging.info(str(datetime.now()) + " ############## START crawling sites #################################################")
        for site in self.sites:
            logging.info(str(datetime.now()) + " ============= Processing site : " + site + " ======================================")
            
            if site in self.siteLastCrawled:
                lastCrawledTimeStamp = self.siteLastCrawled[site]
            else:
                lastCrawledTimeStamp = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            
            try:
                parser_output = feedparser.parse(site)
            except Exception as e:
                print "Feedparser could not parse " + site
                continue
                
            entries = parser_output.entries
            
            # This will update the latest time stamp crawled, and insert the entry if no information was available for this site.
            self.siteLastCrawled[site] = datetime.now()
           
            self.processEntries(entries , lastCrawledTimeStamp )

    def processEntries(self , entries , timestamp):
    
        # Remove all HTML tags from the text
        pattern = re.compile(u'<\/?\w+\s*[^>]*?\/?>', re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
        for entry in entries:
        
            title = "NA"
            description = "NA"
            link = "NA"
            published ="NA"
            articleContent = "NA"
            category = "NA"
            
            
            if "published" in entry:
                published = self.removeNonAscii(entry['published'])
                published_parsed_struct = entry['published_parsed']
                
                # In certain instances, published_parsed date is not available, entry is considered  valid 
                if published_parsed_struct == None:
                    break
                
                published_parsed = datetime.fromtimestamp(mktime(published_parsed_struct))
                        
              
                # Time filter to prevent redundant data collection
                if published_parsed < timestamp:
                    return            
            
            
            if "title" in entry:
                title = self.removeNonAscii(entry['title'])
            
                
        
            if "description" in entry:
                description = pattern.sub(u" " , self.removeNonAscii(entry['description']))
            
            if "category" in entry:
                category = self.removeNonAscii(entry['category'])
            
            if "link" in entry:
                link = self.removeNonAscii(entry['link'])
                httpParserObj = htmlParser(link, 'article')
                articleContent = self.removeNonAscii(httpParserObj.fetchText())
            
            
            
                
            
            #Skip dumping the entry if no keyword is present.
            #TODO For training data collection, turning off text filtering. filtering is done on basis of title only
            
            keyword = self.isContainsKeyword(title)
            if not(keyword == ""):
                return
            
             
             
             
            #self.dumpParsedResult( ['"'+title+'"' , '"'+description+'"' , '"'+link+'"' , '"'+published+'"' , '"'+articleContent+'"' ])
            self.dumpParsedResult( [title , description , link , published , category , keyword , articleContent  ])
    
    def dumpParsedResult(self , entry_value_list):
    
        self.numOfMsgCrawled = self.numOfMsgCrawled + 1
        logging.debug(" Message : " + ', '.join(entry_value_list))
        with open(header.outputFilePath , 'ab') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter="," , quotechar='"', quoting=csv.QUOTE_ALL)
            csvWriter.writerow(entry_value_list)





    def removeNonAscii(self , text):

        return ''.join([i if ord(i) < 128 else ' ' for i in text])       

            
    def isContainsKeyword(self , text):
    
        for keyword in self.keywordList:
            if(keyword in text.lower()):
                return keyword
    
        return ""          


    



# TODO :
# Filter text : Remove hyperlinks
# Implement Exception Handling
# Implement Timestamp filter, if required










# Parse Site Information file for which data is to be crawled.


# Invoke processSites to start crawling data.




     
