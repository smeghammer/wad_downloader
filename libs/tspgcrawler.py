'''
Created on 9 Jan 2021

@author: smegh

the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
enntry as retrieved appropriately. That way, I do not have to run the retriever in one go.
'''
import lxml
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup

'''
the crawler is desiged to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
enntry as retrieved appropriately. That way, I do not have to run the retriever in one go.
'''


class SentinelsPlaygroundCrawler(AbstractCrawler):

    '''
    initialise class instance with the url, root of API, root for downloads and a database 
    object - we only want to instantiate the database object one time, so pass it around after
    instantiating in the start module:
    '''
    
    def __init__(self,startnode,crawlroot,downloadRoot,database,counter=1):
        self.url = crawlroot + startnode
        self.downloadRoot = downloadRoot
        self.crawlroot = crawlroot
        self.db = database
        self.soup = None
        self.counter=counter
        
    '''
    stub
    '''
    def findSpiderLinks(self):
        print('spider links')
    
    '''
    stub
    '''
    def findDownloadLinks(self):
        print('download links')
        
    '''
    push the download link to the database, assembling as needed and
    flag as not fetched
    '''
    def storeDownloadLink(self,linkData):               
        print(linkData)
        obj = { 
            '_id':linkData['_id'], 
            'url' : self.downloadRoot + linkData['filename'], 
            'state' : 'NOTFETCHED', 'source':'tspg',  
            'metadata':linkData  
            }
        self.db.storeDownloadLinkObj(obj)
    
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'lxml')
        self.crawl()

    def crawl(self):
        print('crawling...')
        '''
        for TSPG, the download pages are all
        
        https://allfearthesentinel.net/zandronum/download.php?file=xxxx
        
        where xxx is filename. 
        
        I know there are 270 pages of downloads, so I  can  count up to this
        and build corresponding URLs.
        
        I don't need to recurse.
        '''

        while self.counter < 271:
            '''  look for download links and store them
            You may need to fiddle with this selector as the column has changed at least
            once...
              '''
            downloadLinks = self.data.select('#zandronum td:nth-child(2) a:nth-child(2)')
            if not len(downloadLinks):
                crawl = False
            for downloadLink in downloadLinks:
                ''' find hrefs and any metadata: '''
                print(downloadLink['href'])
                self.storeDownloadLink({
                    '_id' : downloadLink['href'][29:],
                    'href' : downloadLink['href'],
                    'filename' : downloadLink['title'][9:],
                    'dir' : 'page' + str(self.counter) + '/'
                    })
            
            ''' and load the next page '''
            self.counter+=1
            response = requests.get(self.url + '?page=' + str(self.counter))
            self.data = BeautifulSoup(response.content,'lxml')

            
            

        
    