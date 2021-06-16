'''
Created on 9 Jan 2021

@author: smegh
'''
import requests
from libs.abstractcrawler import AbstractCrawler
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import json

'''
the crawler is designed to collect metadata only - having a recursive download function
is a crazy idea...

Once the file metadata is stored in mongo, I can run a downloader against that and flag each
entry as retrieved appropriately. That way, I do not have to run the retriever in one go.

This superclass uses the base class methods __init__() and storeDownloadLink()
'''
class R667Crawler(AbstractCrawler):
    
    '''
    load the URL and - for the case of JSON, load it as a dict.
    '''
    def open(self):
        response = requests.get(self.url)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl__(self):
        print('TEST')
        fish = b'<h2 class="rl_tabs-title nn_tabs-title">\n<a class="anchor rl_tabs-sm-scroll nn_tabs-sm-scroll" id=" anchor-info"></a>\nInfo</h2><br/><strong>Name:</strong> 40mm Grenade Launcher<br/><strong>Class: </strong> 5<br/><strong>Type:</strong> Projectile<br/><strong>Palette:</strong>  Doom<br/><strong>Summon:</strong> 40mmGrenadeLauncher<br/><strong>Ammotype:</strong>  40mmGrenades<br/><strong>AltFire:</strong> Yes<br/><strong>Powered Mode:</strong>  No<br/><strong>Brightmaps:</strong> No<br/><strong>Added States:</strong> No<br/><strong>ACS: </strong> No<br/>'
        self.extractItemInfo(fish)


    def crawl(self):
        print('crawling...')
        '''
        For R667, I want to collect the metadata for each download (and possibly the download binary itself).
        '''
        
        '''
        Identify any download links and associated surrounding HTML that defines
        metadata and extract that as JSON
         - the download link can go into the mongoDD, and wan probably put the metadata JSON in there too to associate 
         them together...
        '''
        #.item-194
        crawlLinks = self.data.select('div.bd-vmenu-1:nth-child(2) li > div > ul > li ');
        _counter = 1
        _data = None
        _soup = None
        _response = None
        _pagination = None
        _dataDOMblocks = dict() 
        _dataitems = dict() #output
        
        _crawllinks = dict()
        for crawlLink in crawlLinks:
            print('getting R667 crawl links...', _counter)
            _href = 'https://www.realm667.com' + crawlLink.find('a')['href']
            _response = requests.get(_href)
            _soup = BeautifulSoup(_response.content,'html.parser')
            #now LOAD this link:
            '''
            NEEED TO RESET THIS!!
            '''
            _topic = _soup.select('li.parent > a.active')[0].text.strip()
            _section = _soup.select('div.bd-container-inner > h2')[0].text.strip()
            _crawllinks[_href] = {'crawled' : False,'topic':_topic,'section':_section}
            
            '''
            here, we find footer pagination links for more pages holding repository items
            and also the repo items on the current page. TODO: work out what is put into DB and what is processed at runtime
            '''

            '''
            find paginarion links:
            '''
            _pagination = _soup.select('div > ul.pagination > li > a')
            
            if _pagination:
                for _page in _pagination:
                    print(_page['href'])
                    _href = 'https://www.realm667.com' + _page['href']
                    _crawllinks[_href] = {'crawled' : False,'topic':_topic,'section':_section}
                    _counter+=1   
            
            ''' and for each crawl link:
             - get the items on the page
             - identify any pagination links and follow these '''
            _soup = None
            _counter+=1
        
        ''' once we have the crawl links list, load each one and extract the relevant metadata from the DOM:: '''
        _c = 0
        for _crawllink in _crawllinks:
            print(_crawllinks[_crawllink])
            _c+=1
            
            '''  second pass: get the individual item blocks:'''
            _response = requests.get(_crawllink)
            _soup = BeautifulSoup(_response.content,'html.parser')
            _currdataitems = _soup.select('div.separated-item-8')
            for _currdataitem in _currdataitems:
                ''' and fron each item block, extract somedetails about the thing '''
                _itemtitle = _currdataitem.select('article > h2')[0].text.strip()
                print(_currdataitem)
                _info = {}
                try:
                    ''' INFO '''
                    _info = self.extractItemInfo(_currdataitem.select('div.tab-content > div.tab-pane:nth-of-type(2)')[0].encode_contents())
                except:
                    pass
                
                ''' CREDITS '''
                _credits = {}
                try:
                    _credits = self.extractItemInfo(_currdataitem.select('div.tab-content > div.tab-pane:nth-of-type(3)')[0].encode_contents())
                except:
                    pass
                
                print(_info)
                _dataitems[_itemtitle] = {
                    'info':_info,
                    'credits':_credits,
                    'topic':_crawllinks[_crawllink]['topic'],
                    'section':_crawllinks[_crawllink]['section']
                }
            
            
            
            '''
            Once we have the list of pages, load each one and grab the data from the DOM
            [I might want to cache the pages, otherwise I will be loading the top level ones twice...]
            '''
        with open('output.json','w') as f :
            f.write(json.dumps(_dataitems))
            
        
            '''
            Finally, put the JSON im in the database
            '''
        print('done')
        
    def extractItemInfo(self,bytestr):
        htmlstr = bytestr.decode('utf-8')
        print('---------ITEM INPUT-------------')
        print(htmlstr)
        print('---------END ITEM INPUT-------------')
        _soup = BeautifulSoup(htmlstr,'html.parser')
        _title = _soup.select('h2')[0].text.strip()
        print('---------TITLE-------------')
        print(_title)
        print('---------/TITLE-------------')
        _out = {'title':_title,'entries':[]}
        ''' split on BR (crappy HTML) '''
        _items = htmlstr.split('<br/>')
        _items.pop(0)   #remove first entry as we already have the title:
        for _item in _items:
            print('---------ITEM-------------')
            print(_item)
            print('---------/ITEM-------------')
            try:
                ''' will ignore the first entry (title) '''
                _s = BeautifulSoup(_item,'html.parser')
                ''' assumes a given structure '''
                print(_s.find('strong'))
                print(_s.contents[1].strip())
                _out['entries'].append({_s.find('strong').text : _s.contents[1].strip()})
            except Exception as ex:
                print(ex)
                pass
        print(_out)
        return(_out)
        
        
        
        
        

