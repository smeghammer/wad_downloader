'''
Created on 10 Jan 2021

@author: smegh
'''

from abc import ABC, abstractmethod

class AbstractCrawler(ABC):
    
    @abstractmethod
    def findSpiderLinks(self):
        return
    
    @abstractmethod
    def findDownloadLinks(self):
        return
    
    @abstractmethod
    def storeDownloadLink(self,linkData=None):
        return
    
    @abstractmethod
    def open(self):
        return
    
    @abstractmethod
    def crawl(self):
        return