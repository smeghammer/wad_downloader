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
    def __init__(self,crawlerId,startnode,crawlroot,downloadRoot,database,args=None):
        self.url = crawlroot + startnode
        self.downloadRoot = downloadRoot
        self.crawlroot = crawlroot
        self.db = database
        self.soup = None
        self.counter=0
        self.crawlerId = crawlerId
        self.args = args    #just in case I need them

    
#     @abstractmethod
#     def storeDownloadLink(self,linkData=None):
#         return

    '''
    push the download link to the database, assembling as needed and
    flag as not fetched
    '''
    @classmethod
    def storeDownloadLink(self,linkData=None, downloadRoot='', crawlerId='', db=None,coll=None):
        print(linkData)
        obj = { 
            '_id':linkData['_id'], 
            'url' : linkData['href'], 
            'state' : 'NOTFETCHED', 
            'source':crawlerId,  
            'metadata':linkData  
            }
#         if coll and coll=='r667':
#             db.storeRepoPageObj(obj)
#         else:
#             db.storeDownloadLinkObj(obj)
        db.storeDownloadLinkObj(obj)
    
    @abstractmethod
    def open(self,sourceKey):
        return
    
    @abstractmethod
    def crawl(self):
        return