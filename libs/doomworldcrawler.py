'''
Created on 9 Jan 2021

@author: smegh

the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
enntry as retrieved appropriately. That way, I do not have to run the retriever in one go.
'''
import json
import requests
from libs.abstractcrawler import AbstractCrawler

'''
the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
enntry as retrieved appropriately. That way, I do not have to run the retriever in one go.
'''
class DoomworldCrawler(AbstractCrawler):

    '''
    initialise class instance with the url, root of API, root for downloads and a database 
    object - we only want to instantiate the database object one time, so pass it around after
    instantiating in the start module:
    '''
    
    def __init__(self,startnode,crawlroot,downloadRoot,database):
        self.url = crawlroot + startnode
        self.downloadRoot = downloadRoot
        self._dwapiroot = crawlroot
        self.db = database
        
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
    push the download link to the database, assembling as needed and
    flag as not fetched
    '''
    def storeDownloadLink(self,linkData):                                                    #or PENDNG or FETCHED
        print(self.downloadRoot + linkData['dir']+linkData['filename'])
        obj = {  'url' : self.downloadRoot + linkData['dir']+linkData['filename'], 'state' : 'NOTFETCHED', 'source':'doomworld',  'metadata':linkData  }
        self.db.storeDownloadLinkObj(obj)
    
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
        We know the JSON structure for ID Games API, so test for either files or directories
        (pretty sure there are no dirs that list dub-dirs AND files but this sould handle that
        anyway):
        '''
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']: 
                print(item['id'])
                '''
                recursively instantiate the crawler with each new directory URL:
                '''
                _crawler = DoomworldCrawler(self._dwapiroot + str(item['id']),self._dwapiroot,self.downloadRoot,self.db)
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            for item in self.data['content']['file']: 
                try:
                    '''
                    se have a file listing, so process it (into mongoDB) for
                    subsequent download:
                    '''
                    print(item['title'])
                    self.storeDownloadLink(item)
                except Exception as ex:
                    print(ex)
            
           
    

    