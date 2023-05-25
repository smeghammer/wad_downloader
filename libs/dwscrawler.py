'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup

class WADStationCrawler(AbstractCrawler):

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('Doom WAD station crawling...')
        ''' for DOOM WAD Station, the download pages are all
        
        http://www.doomwadstation.net/mega//ssssss
        
        where sss is a filename. It is a single page. I don't need to recurse, therefore I can use the base class methods
        look for download links and store them  '''
        downloadLinks1 = self.data.select('tr.file_bg1  a')
        downloadLinks2 = self.data.select('tr.file_bg2  a')
        downloadLinks = downloadLinks1+ downloadLinks2
        
        for downloadLink in downloadLinks:
            ''' find hrefs and any metadata: '''
            # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
            print(downloadLink['href'])
            self.store_download_link(
                {'_id' : downloadLink['href'][2:],
                 'href' : downloadLink['href'][2:], 
                 'filename' : downloadLink['href'][2:], 
                 'dir' : 'page1' + '/' 
                 },
                self.downloadRoot + downloadLink['href'][2:], 
                )

            
