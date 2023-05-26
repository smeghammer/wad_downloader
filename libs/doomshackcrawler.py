'''
Created on 18 Jan 2021

@author: smegh
'''
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup

class DoomShackCrawler(AbstractCrawler):

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('Doomshack repo crawling...')
        downloadLinks = self.data.select('li > a')
        counter = 0
        for downloadLink in downloadLinks:
            if counter > 0:    #skipn the parent dir link
                ''' find hrefs and any metadata: '''
                # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
                print(downloadLink['href'])
                
                _obj =  {'_id' : downloadLink['href'],
                     'href' : self.download_root + downloadLink['href'], 
                     'filename' : downloadLink['href'].split('/')[2], 
                     'dir' : 'page1' + '/' 
                     }
                
                self.store_download_link(
                  _obj ,
                    self.download_root + downloadLink['href'], 
                    ) 
            counter+=1