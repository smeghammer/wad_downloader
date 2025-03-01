'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from bs4 import BeautifulSoup
# model
from libs.model import model

from libs.abstractcrawler import AbstractCrawler
from libs.model.model import MetaData, WADDownload

class CamoyCrawler(AbstractCrawler):

    ''' load the URL and - for the case of JSON, load it as a dict. '''
    def open(self):
        response = requests.get(self.url,timeout=30)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        breakpoint()
        qs = model.WADDownload.objects()
        
        print('Camoy repo crawling...')
        download_links = self.data.select('pre > a')
        counter = 0
        for download_link in download_links:
            if counter > 0:    #skipn the parent dir link
                # find hrefs and any metadata:
                # see https://stackoverflow.com/questions/4747397/calling-base-class-method-in-python
                print(download_link['href'])
                # self.store_download_link(
                #     {'_id' : download_link['href'],
                #      'href' : self.download_root + download_link['href'], 
                #      'filename' : download_link['href'], 
                #      'dir' : 'page1' + '/' 
                #      },
                #     self.download_root + download_link['href'],
                #     )
                # exists = qs.with_id(self.download_root + download_link['href'])
                breakpoint()
                # if not qs.with_id(model.WADDownload,self.download_root + download_link['href']):
                meta = model.MetaData(
                    _id =self.download_root + download_link['href'],
                    href = self.download_root + download_link['href'],
                    filename = download_link['href'],
                    dir = 'page1' + '/',
                )
                download = model.WADDownload(
                    # _id = download_link['href'],
                    _id = self.download_root + download_link['href'],
                    url = self.download_root + download_link['href'],
                    source = self.crawler_id,
                    metadata = meta,
                )
                # else:
                #     print(f"'{self.download_root + download_link['href']}' already stored")
                # breakpoint()
                # self.store_download_model()

                result = download.save()
                print(result)
                breakpoint()
            counter+=1

    # def get_metadata_model_for_crawler(self, metadata) -> MetaData:
    #     return model.MetaData(
    #             href = self.download_root + metadata['href'],
    #             filename = metadata['href'],
    #             dir = 'page1/',
    #         )
    
    # def store_download_model(self, download: dict, meta: dict) -> WADDownload:
    #     return model.WADDownload(
    #             _id = self.download_root + meta['href'],
    #             url = self.download_root + meta['href'],
    #             source = self.crawler_id,
    #             metadata = self.get_metadata_model_for_crawler(meta),
    #         ).save()