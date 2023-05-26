'''
Created on 9 Jan 2021

@author: smegh
'''
import json
import requests
import uuid
from libs.abstractcrawler import AbstractCrawler

class DBACrawler(AbstractCrawler):
    ''' superclass enabling crawling of doomworld IDGames mirror, with this one storing the files by author '''
    def open(self):
        ''' load the URL and - for the case of JSON, load it as a dict. '''
        response = requests.get(self.url,timeout=30)
        self.data = json.loads(response.content)

        # Once the data is loaded to the class instance, call the recursive function:
        self.crawl()

    def crawl(self):
        ''' Recursive function to parse the loaded JSON and store WAD data for subsequent download '''
        print('Doomworld crawling...')

        # We know the JSON structure for ID Games API, so test for either files or directories
        # (pretty sure there are no dirs that list dub-dirs AND files but this sould handle that  anyway):
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']:
                print(item['id'])

                # recursively instantiate the crawler with each new directory URL:
                _crawler = DBACrawler(str(item['id']),self.crawlroot,self.download_root,self.db, self.crawler_id)
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            for item in self.data['content']['file']:
                # We have a file listing, so process it (into mongoDB) for subsequent download:
                try:
                    print(item['title'])
                    
                    # first, we need the URL to download:
                    orig_url = self.download_root + item['dir']+item['filename']
                    
                    # then reset the store directory to the author prefix:
                    item['dir'] = self.get_name_prefix(item)
                    # self.get_name_prefix(item)
                    self.store_download_link(item, orig_url)
                    # self.store_download_link(item, self.downloadRoot + item['dir']+item['filename'])
                    # self.store_download_link(item, self.downloadRoot + self.get_name_prefix(item) +item['filename'])
                except TypeError as err:
                    print(err)
                except UnicodeEncodeError as err:
                    print(err)
                    # replace the field with something else in the case of unicode error:
                    # assume TITLE, anythiong else will break the download anyway...
                    item['title'] = f"UTF8Error_{uuid.uuid4()}"
                
    def get_name_prefix(self,data):
        try:
            return  f"{((data.get('author','XXX')[0:3])).upper()}/" 
        except TypeError as ex:
            # sometimes, author may ne none, or not UTF8, so return something else here:
            return 'XXX'
