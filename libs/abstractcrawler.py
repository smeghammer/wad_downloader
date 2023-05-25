'''
Created on 10 Jan 2021

@author: smegh
'''

from abc import ABC, abstractmethod
# import requests
 #from bs4 import BeautifulSoup

class AbstractCrawler(ABC):

    # @abstractmethod
    # def findSpiderLinks(self):
    #     return
    #
    # @abstractmethod
    # def findDownloadLinks(self):
    #     return

    @classmethod
    def __init__(self,startnode,crawlroot,download_root,database,crawler_id,counter=1):
        '''  initialise class instance with the url, root of API, root for downloads and a database 
        object - we only want to instantiate the database object one time, so pass it around after
        instantiating in the start module:  '''
        self.data = None
        self.url = crawlroot + startnode
        self.downloadRoot = download_root
        self.crawlroot = crawlroot
        self.db = database
        self.crawlerId = crawler_id
        self.counter=counter
        self.soup = None


    @classmethod
    def store_download_link(self,link_data,url):
        '''  push the download link to the database, assembling as needed and flag as not fetched  '''
        obj = {
            'url' : url, 
            'state' : 'NOTFETCHED', 
            'source':self.crawlerId,    
            'metadata':link_data  
        }
        print(obj)
        self.db.store_download_link_obj(obj)

    @abstractmethod
    def open(self):
        ''' implemented in concrete implementations of this abstract class '''
        return

    @abstractmethod
    def crawl(self):
        ''' implemented in concrete implementations of this abstract class '''
        return
