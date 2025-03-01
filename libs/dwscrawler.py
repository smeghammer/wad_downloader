'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from bs4 import BeautifulSoup
from libs.model import model
from libs.abstractcrawler import AbstractCrawler

class WADStationCrawler(AbstractCrawler):
    ''' crawler implementation for Doom WAD Station '''

    def open(self):
        ''' load the URL and - for the case of JSON, load it as a dict. '''
        response = requests.get(self.url,timeout=30)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        ''' for DOOM WAD Station, the download pages are all
        
        http://www.doomwadstation.net/mega//ssssss
        
        where sss is a filename. It is a single page. I don't need to recurse, therefore I can use the base class methods
        look for download links and store them  '''
        print('Doom WAD station crawling...')
        download_links_1 = self.data.select('tr.file_bg1  a')
        download_links_2 = self.data.select('tr.file_bg2  a')
        download_links = download_links_1+ download_links_2

        for download_link in download_links:
            # find hrefs and any metadata:
            # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
            print(download_link['href'])
            breakpoint()
            meta = model.MetaData(
                href = self.download_root + download_link['href'][2:],
                filename = download_link['href'],
                dir = 'page1' + '/',
            )

            download = model.WADDownload(
                _id = self.download_root + download_link['href'][2:],
                url = self.download_root + download_link['href'][2:],
                source = self.crawler_id,
                metadata = meta,
            )
            # self.store_download_link(
            #     {'_id' : download_link['href'][2:],
            #      'href' : download_link['href'][2:], 
            #      'filename' : download_link['href'][2:], 
            #      'dir' : 'page1' + '/' 
            #      },
            #     self.download_root + download_link['href'][2:],
            #     )
            result = download.save()
            print(result)
