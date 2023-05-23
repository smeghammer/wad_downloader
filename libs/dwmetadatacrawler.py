'''
Created on 9 Jan 2021

@author: smegh
'''
import json
import requests

import sqlite3

from libs.abstractcrawler import AbstractCrawler

class DWMetadataCrawler(AbstractCrawler):
    
    def __init__(self,*args, **kwargs):
        ''' I want to have an instance od SQLite3 HERE, but not for the pother
        crawlers. So override the init() method to also initialise a SQLite3
        instance 
        
        see:
        https://stackoverflow.com/questions/12701206/how-to-extend-python-class-init
        '''
        print('metadata init...',args)
        super().__init__(*args, **kwargs)
        
        # and initialise the SQLite3 code:
        
        
    

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url)
        self.data = json.loads(response.content)
        
        ''' Once the data is loaded to the class instance, call the recursive function: '''
        self.crawl()
    
    ''' Recursive function to parse the loaded JSON and store WAD data for subsequent download '''
    def crawl(self):
        print('Doomworld crawling...')
        
        ''' We know the JSON structure for ID Games API, so test for either files or directories
        (pretty sure there are no dirs that list dub-dirs AND files but this sould handle that anyway): '''
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']: 
                print(item['id'])
                
                '''  recursively instantiate the crawler with each new directory URL: '''
                _crawler = DWMetadataCrawler(str(item['id']),self.crawlroot,self.downloadRoot,self.db, self.crawlerId)
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            for item in self.data['content']['file']: 
                '''
                Here, I need to grab the metadata, rather than download the file, and insert (or update) that into
                a SQLite3 instance. Once I have a relational table, I can further determine extra infor from that 
                metadata.
                '''
                try:
                    ''' We have a file listing, so process it (into SQLite3) for subsequent metadata processing. 
                    Matybe a relational database, FKed on USER??: '''
                    print(item['date'],item['author'])
                    # self.storeDownloadLink(item, self.downloadRoot + item['dir']+item['filename'])
                except Exception as ex:
                    print(ex)
            
    