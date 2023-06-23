'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from bs4 import BeautifulSoup
from libs.abstractcrawler import AbstractCrawler

class CamoyCrawler(AbstractCrawler):

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url,timeout=30)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('Camoy repo crawling...')
        download_links = self.data.select('pre > a')
        counter = 0
        for download_link in download_links:
            if counter > 0:    #skipn the parent dir link
                # find hrefs and any metadata:
                # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
                print(download_link['href'])
                self.store_download_link(
                    {'_id' : download_link['href'],
                     'href' : self.download_root + download_link['href'], 
                     'filename' : download_link['href'], 
                     'dir' : 'page1' + '/' 
                     },
                    self.download_root + download_link['href'],
                    )
            counter+=1
