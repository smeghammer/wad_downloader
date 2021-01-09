'''
Created on 9 Jan 2021

@author: smegh

TODO: abstract this to an ABC

'''

from bs4 import BeautifulSoup   #will need his when website scarping
import json
import requests
#import pymongo

'''
the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
enntry as retrieved appropriately. That way, I do not have to run the retriever in one go.
'''
class Crawler():
    
    crawling = False
    
    '''
    initialise class instance with the url
    '''
    def __init__(self,url):
        self.url = url
        #set the crawling flag to true:
        self.crawling = True
        
    '''
    stub
    '''
    def findSpiderLinks(self):
        print('spider links')
    
    '''
    stub
    '''
    def findDownloadLinks(self):
        print('download links')
    
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = json.loads(response.content)
        
        '''
        Once the data is loaded to the class instance, call the recursive function:
        '''
        self.crawl()
    
    '''
    Recursive function to parse the loaded JSON and store WAD data for subsequent download
    '''
    def crawl(self):
        print('crawling...')
        
        '''
        We know the JSON structure for ID Games API, so test for eithe rfiles or directories
        (pretty sure there are no dirs that list dub-dirs AND files but this soul dhandle that
        anyway):
        '''
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']: 
                print(item['id'])
                '''
                recursively instantiate the crawler with each new directory URL:
                '''
                _crawler = Crawler(_dwapiroot + str(item['id']))
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            for item in self.data['content']['file']: 
                try:
                    '''
                    se have a file listing, so process it (into mongoDB) for
                    subsequent download:
                    '''
                    print(item['title'])
                except Exception as ex:
                    print(ex)
#                 _crawler = Crawler(_dwapiroot + str(item['id']))
            
           
        
def recurse():
    print('recursing')
        
if __name__ == '__main__':
    print('starting spider')
    
#     soup = BeautifulSoup()
    
    
    #start at the /levels directory (id=6)
    _dwapiroot = 'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id='
    crawler = Crawler(_dwapiroot + '6')
    crawler.open()

    