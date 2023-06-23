'''
Created on 18 Jan 2021

@author: smegh
'''
import requests
from bs4 import BeautifulSoup
from libs.abstractcrawler import AbstractCrawler

class DoomShackCrawler(AbstractCrawler):

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url,timeout=30)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('Doomshack repo crawling...')
        download_links = self.data.select('li > a')
        counter = 0
        for download_link in download_links:
            if counter > 0:    #skipn the parent dir link
                # find hrefs and any metadata:
                # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
                print(download_link['href'])

                _obj =  {'_id' : download_link['href'],
                     'href' : self.download_root + download_link['href'], 
                     'filename' : download_link['href'].split('/')[2],
                     'dir' : 'page1' + '/' 
                     }

                self.store_download_link(
                  _obj ,
                    self.download_root + download_link['href'],
                    )
            counter+=1
