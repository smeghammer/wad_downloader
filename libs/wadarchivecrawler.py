'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

'''
the crawler is designed to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.

This superclass uses the base class methods __init__() and storeDownloadLink()
'''
class WADArchiveCrawler(AbstractCrawler):
    
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
        for wad-archive, the download pages are all
        
        https://www.wad-archive.com/Category/WADs/nnn
        
        where nnn is a number. I can therefore count up until there are no download elements - if the number is 
        too great, the body content is not present, but we still get a 200OK response. Therefore I an test the downloadlinks 
        var for meing null/sero-length.
        
        I don't need to recurse, therefore I can use the base class methods
        TODO: I need to find out about recursive base class methods!!
        
        I might need to filter out pages that throw up an ad.
        '''

        crawl = True
        while crawl:
            '''  look for download links and store them  '''
            downloadLinks = self.data.select('div.result-image > a')
            if not len(downloadLinks):
                crawl = False
            for downloadLink in downloadLinks:
                ''' find hrefs and any metadata: '''
                print(downloadLink['href'])
                AbstractCrawler.storeDownloadLink({ 
                    '_id' : downloadLink['href'][5:],  'href' : downloadLink['href'] + '/',  'filename' : downloadLink['title'], 'dir' : 'page' + str(self.counter) + '/'},
                    self.downloadRoot,
                    self.crawlerId,
                    self.db         #from base class
                )
            
            ''' and load the next page '''
            self.counter+=1
            response = requests.get(self.url + str(self.counter))
            self.data = BeautifulSoup(response.content,'html.parser')
            

