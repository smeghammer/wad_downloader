'''
Created on 10 Jan 2021

@author: smegh
'''

from abc import ABC, abstractmethod
# import requests
# from bs4 import BeautifulSoup

class AbstractCrawler(ABC):

    # @abstractmethod
    # def findSpiderLinks(self):
    #     return
    #
    # @abstractmethod
    # def findDownloadLinks(self):
    #     return
    '''  initialise class instance with the url, root of API, root for downloads and a database 
    object - we only want to instantiate the database object one time, so pass it around after
    instantiating in the start module:  '''
    # @classmethod
    def __init__(self,startnode,crawlroot,download_root,database,crawler_id,counter=1):
        self.url = crawlroot + startnode
        self.download_root = download_root
        self.crawlroot = crawlroot
        self.db = database
        self.crawlerId = crawler_id
        self.counter=counter
        self.soup = None

    # @abstractmethod
    # def storeDownloadLink(self,linkData=None,url=None):
    #     return

    @classmethod
    def storeDownloadLink(self,linkData,url):                                                    #or PENDNG or FETCHED
        '''  push the download link to the database, assembling as needed and flag as not fetched  '''
        obj = {
            'url' : url, 
            'state' : 'NOTFETCHED', 
            'source':self.crawlerId,    
            'metadata':linkData  
        }
        print(obj)
        self.db.storeDownloadLinkObj(obj)

    @abstractmethod
    def open(self):
        return

    # @classmethod
    # def open(self):
    #     response = requests.get(self.url)
    #     self.data = BeautifulSoup(response.content,'html.parser')
    #     self.crawl(self)

    @abstractmethod
    def crawl(self):
        return
