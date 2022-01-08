'''
Created on 9 Jan 2021

@author: smegh

the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.

for wad-archive, the download pages are all
        
        https://www.wad-archive.com/Category/WADs/nnn

where nnn is a number. I can therefore count up until there are no download elements - if the number is 
too great, the body content is not present, but we still get a 200OK response. Therefore I an test the downloadlinks 
var for meing null/sero-length.

I don't need to recurse.
        https://assets.wad-archive.com/wadarchive/files/4615452b3c86d2a002e0710ac5ba0f31b7e2ae8a/invasion-addon_v0.4-alpha.pk3
I might need to filter out pages that throw up an ad. '''

import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup


class WADArchiveCrawler(AbstractCrawler):
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        print('WAD Archive crawling...')
        crawl = True
        while crawl:
            '''  look for download links and store them  '''
            downloadLinks = self.data.select('div.result-image > a')
            if not len(downloadLinks):
                crawl = False
            for downloadLink in downloadLinks:
                ''' find hrefs and any metadata: '''
                self.storeDownloadLink({
                    '_id' : downloadLink['href'][5:],
                    'href' : downloadLink['href'] + '/',
                    'filename' : downloadLink['title'],
                    'dir' : 'page' + str(self.counter) + '/'
                    },
                    self.downloadRoot + downloadLink['href'][5:] + '/' + downloadLink['title'], 
                )
            
            ''' and load the next page '''
            self.counter+=1
            response = requests.get(self.url + str(self.counter))
            self.data = BeautifulSoup(response.content,'html.parser')
            

            
            

        
    