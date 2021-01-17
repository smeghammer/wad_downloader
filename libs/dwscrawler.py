'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

'''
the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.

This superclass uses the base class mehods __init__() and storeDownloadLink()
'''
class WADStationCrawler(AbstractCrawler):
    
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('crawling...')
        '''
        for DOOM WAD Station, the download pages are all
        
        http://www.doomwadstation.net/mega//ssssss
        
        where sss is a filename. It is a single page....
        
        I don't need to recurse, therefore I can use the base class methods
        TODO: I need to find out about recursive base class methods!!
        '''
        '''  look for download links and store them  '''
#         downloadLinks = self.data.find_all(['tr.file_bg1  a','tr.file_bg2  a'])
        downloadLinks1 = self.data.select('tr.file_bg1  a')
        downloadLinks2 = self.data.select('tr.file_bg2  a')
        downloadLinks = downloadLinks1+ downloadLinks2
        
        for downloadLink in downloadLinks:
            ''' find hrefs and any metadata: '''
            # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
            print(downloadLink['href'])
            AbstractCrawler.storeDownloadLink(
                {'_id' : downloadLink['href'][2:],'href' : downloadLink['href'][2:], 'filename' : downloadLink['href'][2:], 'dir' : 'page1' + '/' },
                self.downloadRoot,
                self.crawlerId,
                self.db         #from base class
                )

            

