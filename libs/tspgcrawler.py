'''
Created on 9 Jan 2021

@author: smegh
'''
import json
import lxml
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup

'''
the crawler is designed to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.

This superclass uses the base class methods __init__() and storeDownloadLink()
'''


class SentinelsPlaygroundCrawler(AbstractCrawler):
    
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'lxml')
        self.crawl()

    def crawl(self):
        print('crawling...')
        '''
        for TSPG, the download pages are all
        
        https://allfearthesentinel.net/zandronum/download.php?file=xxxx
        
        where xxx is filename. 
        
        I know there are 270 pages of downloads, so I  can  count up to this
        and build corresponding URLs.
        
        I don't need to recurse, therefore I can use the base class methods
        TODO: I need to find out about recursive base class methods!!
        '''

        while self.counter < 271:
            '''  look for download links and store them
            You may need to fiddle with this selector as the column has changed at least
            once...
              '''
            downloadLinks = self.data.select('#zandronum td:nth-child(2) a:nth-child(2)')
            if not len(downloadLinks):
                crawl = False
            for downloadLink in downloadLinks:
                ''' find hrefs and any metadata: '''
                print(downloadLink['href'])
                self.storeDownloadLink({
                    '_id' : downloadLink['href'][29:],
                    'href' : downloadLink['href'],
                    'filename' : downloadLink['title'][9:],
                    'dir' : 'page' + str(self.counter) + '/'
                    },
                    self.downloadRoot,
                    self.crawlerId,
                    self.db         #from base class
                )
            
            ''' and load the next page '''
            self.counter+=1
            response = requests.get(self.url + '?page=' + str(self.counter))
            self.data = BeautifulSoup(response.content,'lxml')

            
            

        
    