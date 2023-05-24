'''
Created on 9 Jan 2021

@author: smegh
'''
import json
import requests
from libs.abstractcrawler import AbstractCrawler

class DoomworldCrawler(AbstractCrawler):

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
        (pretty sure there are no dirs that list dub-dirs AND files but this sould handle that  anyway): '''
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']: 
                print(item['id'])
                
                '''  recursively instantiate the crawler with each new directory URL: '''
                _crawler = DoomworldCrawler(str(item['id']),self.crawlroot,self.download_root,self.db, self.crawlerId)
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            for item in self.data['content']['file']: 
                try:
                    ''' We have a file listing, so process it (into mongoDB) for subsequent download: '''
                    print(item['title'])
                    self.storeDownloadLink(item, self.download_root + item['dir']+item['filename'])
                except Exception as ex:
                    print(ex)
            
    