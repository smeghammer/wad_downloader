'''
Created on 9 Jan 2021

@author: smegh

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.
For TSPG, the download pages are all
        
        https://allfearthesentinel.net/zandronum/download.php?file=xxxx
        
where xxx is filename.  I know there are MAX_PAGES pages of downloads, so I  can  count up to this
and build corresponding URLs. I don't need to recurse. '''

import lxml
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup

class SentinelsPlaygroundCrawler(AbstractCrawler):
    
    MAX_PAGES = 240
    
    '''  load the URL and content: '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'lxml')
        self.crawl()

    def crawl(self):
        print('TSGP crawling...')
        while self.counter < self.MAX_PAGES:
            '''  look for download links and store them
            You may need to fiddle with this selector as the column has changed at least
            once... '''
            downloadLinks = self.data.select('#zandronum td:nth-child(2) a:nth-child(2)')
            for downloadLink in downloadLinks:
                ''' find hrefs and any metadata: '''
                self.storeDownloadLink({
                    '_id' : downloadLink['href'][29:],
                    'href' : downloadLink['href'],
                    'filename' : downloadLink['title'][9:],
                    'dir' : 'page' + str(self.counter) + '/'
                    },self.downloadRoot + downloadLink['title'][9:]
                )
            
            ''' and load the next page '''
            self.counter+=1
            response = requests.get(self.url + '?page=' + str(self.counter))
            self.data = BeautifulSoup(response.content,'lxml')

            
            

        
    