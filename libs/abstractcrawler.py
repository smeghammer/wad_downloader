'''
Created on 10 Jan 2021

@author: smegh
'''

from abc import ABC, abstractmethod

class AbstractCrawler(ABC):
    
    '''
    initialise class instance with the url, root of API, root for downloads and a database 
    object - we only want to instantiate the database object one time, so pass it around after
    instantiating in the start module.
    
    You may over-ride if needed in the superclass:
    '''
    @classmethod
    def __init__(self,crawlerId,startnode,crawlroot,downloadRoot,database):
        self.url = crawlroot + startnode
        self.downloadRoot = downloadRoot
        self.crawlroot = crawlroot
        self.db = database
        self.soup = None
        self.counter=0
        self.crawlerId = crawlerId

    
#     @abstractmethod
#     def storeDownloadLink(self,linkData=None):
#         return

    '''
    push the download link to the database, assembling as needed and
    flag as not fetched
    '''
    @classmethod
    def storeDownloadLink(self,linkData=None, downloadRoot='', crawlerId='', db=None):
        print(linkData)
        obj = { 
            '_id':linkData['_id'], 
            'url' : downloadRoot + linkData['_id'] + '/' + linkData['filename'], 
            'state' : 'NOTFETCHED', 
            'source':crawlerId,  
            'metadata':linkData  
            }
        db.storeDownloadLinkObj(obj)
    
    @abstractmethod
    def open(self,sourceKey):
        return
    
    @abstractmethod
    def crawl(self):
        return