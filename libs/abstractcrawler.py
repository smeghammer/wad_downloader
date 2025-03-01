'''
Created on 10 Jan 2021

@author: smegh
'''

from abc import ABC, abstractmethod
from libs.model import model
from mongoengine.queryset import QuerySet


class AbstractCrawler(ABC):

    @classmethod
    def __init__(self,startnode,crawlroot,download_root,database,crawler_id,counter=1,metadatadb='metadata.db'):
        '''  initialise class instance with the url, root of API, root for downloads and a database 
        object - we only want to instantiate the database object one time, so pass it around after
        instantiating in the start module:  '''
        self.data = None
        self.url = crawlroot + startnode
        self.download_root = download_root
        self.crawlroot = crawlroot
        self.db = database
        self.metadatadb = metadatadb
        self.crawler_id = crawler_id
        self.counter=counter
        self.soup = None
        

    @classmethod
    def store_download_link(self,link_data,url):
        '''  push the download link to the database, assembling as needed and flag as not fetched  '''
        obj = {
            'url' : url, 
            'state' : 'NOTFETCHED', 
            'source':self.crawler_id,    
            'metadata':link_data  
        }
        print(obj)
        self.db.store_download_link_obj(obj)

        # # do with the MongoDB ODM instead:
        # meta = model.MetaData(
        #         href = self.download_root + download_link['href'],
        #         filename = download_link['href'],
        #         dir = 'page1' + '/',
        #     )
        # download = model.WADDownload(
        #         _id = url,
        #         url = url,
        #         source = self.crawler_id,
        #         metadata = meta,
        #     )

    # @abstractmethod
    # def get_metadata_model_for_crawler(self,metadata:dict) -> model.MetaData:
    #     ''' get the metadata for the specified source. The concrete crawler must implement
    #      the correct logic to construct the model for the given crawler type. This will be
    #      complex (R667) or really simple'''
    #     return

    # @abstractmethod    
    # def store_download_model(self,download:dict) -> model.WADDownload:
    #     ''' construct and store the download model. Concrete implementation must return the
    #      model and the concrete crawler must call save() on the returned model '''
    #     return

    @abstractmethod
    def open(self):
        ''' implemented in concrete implementations of this abstract class '''
        return

    @abstractmethod
    def crawl(self):
        ''' implemented in concrete implementations of this abstract class '''
        return
