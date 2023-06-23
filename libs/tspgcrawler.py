'''
Created on 9 Jan 2021

@author: smegh

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.
For TSPG, the download pages are all
        
        https://allfearthesentinel.net/zandronum/download.php?file=xxxx
        
where xxx is filename.  I know there are MAX_PAGES pages of downloads, so I  can  count up to this
and build corresponding URLs. I don't need to recurse. '''

import requests
from bs4 import BeautifulSoup
from libs.abstractcrawler import AbstractCrawler

class SentinelsPlaygroundCrawler(AbstractCrawler):
    ''' crawler for The Sentinels Playground (https://allfearthesentinel.com - note TLD change!) '''
    MAX_PAGES = 240

    '''  load the URL and content: '''
    def open(self):
        response = requests.get(self.url,timeout=30)
        self.data = BeautifulSoup(response.content,'lxml')
        self.crawl()

    def crawl(self):
        '''  look for download links and store them
        You may need to fiddle with this selector as the column has changed at least
        once... '''
        print('TSGP crawling...')
        while self.counter < self.MAX_PAGES:
            download_links = self.data.select('#zandronum td:nth-child(2) a:nth-child(2)')
            for download_link in download_links:
                # find hrefs and any metadata:
                try:
                    self.store_download_link({
                        '_id' : download_link['href'][29:],
                        'href' : download_link['href'],
                        'filename' : download_link['title'][9:],
                        'dir' : 'page' + str(self.counter) + '/'
                        },self.download_root + download_link['title'][9:]
                    )
                except Exception as ex:
                    # This may fail for legitimate reasons, so log it and continue
                    print(ex)

            # and load the next page:
            self.counter+=1
            response = requests.get(f"{self.url}?page={str(self.counter)}",timeout=30)
            self.data = BeautifulSoup(response.content,'lxml')
