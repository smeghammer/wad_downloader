'''
Created on 9 Jan 2021

@author: smegh
'''
import os
import urllib
import requests
from bs4 import BeautifulSoup
from libs.abstractcrawler import AbstractCrawler

class R667Crawler(AbstractCrawler):
    ''' retrieve Realm 667 queue items from the repository '''
    
    def open(self):
        ''' load the URL and - for the case of JSON, load it as a dict. '''
        response = requests.get(self.url, timeout=30)
        self.data = BeautifulSoup(response.content,'html.parser')
        self.crawl()

    def crawl(self):
        ''' For R667, I want to collect the metadata for each download (and possibly the download binary itself).

        Identify any download links and associated surrounding HTML that defines
        metadata and extract that as JSON
         - the download link can go into the mongoDD, and wan probably put the metadata JSON in there too to associate 
         them together... '''
        print('crawling...')

        # get the category links on the meganav - these should encompass all subcategories
        # Each of these should be loaded, and links extracted as the items to download:
        crawl_links = self.data.select('ul.bd-menu-18.nav:nth-of-type(1) > li:nth-of-type(1) div.container-fluid > div > div')

        items_links = {}

        # TODO: REFACTOR THIS INTO SEPARATE FUNCTIONS:
        # each crawl link has a list of each repo item on it. The code must LOAD each of these in urn and THEN extract the
        # metadata and lins from these...
        for crawl_link in crawl_links:
            print('getting R667 crawl links...')    #, counter)
            _href = 'https://www.realm667.com' + crawl_link.find('a')['href']
            item_response = requests.get(_href,timeout=30)
            _soup = BeautifulSoup(item_response.content,'html.parser')

            #now LOAD this link:
            _section = _soup.select('div.content-category > h2')[0].text.strip()
            items_links[_href] = {'crawled' : False, 'section':_section}

            _soup = None

        # once we have the crawl links list, load each one and extract the relevant metadata from the DOM:
        for items_link in items_links:
            # need to extract the correct section!
            current_section = items_links[items_link]['section']

            # second pass: get the individual item blocks:
            item_response = requests.get(items_link,timeout=30)
            _soup = BeautifulSoup(item_response.content,'html.parser')

            # and now we can extract the individual items from the list:
            item_links = _soup.select('table > tbody > tr > td > a')
            for item_link in item_links:
                # this is the url that will be CRAWLED TO. The download is on each individual page
                print(item_link['href'])
                # here, we actually have a single item, so we just need to get the href and metadata to insert into the database:
                try:
                    item_page = requests.get(f"https://www.realm667.com{item_link['href']}",timeout=30)

                    # load the HTML of the page
                    curr_data_item = BeautifulSoup(item_page.content,'html.parser')
    
                    item_title = curr_data_item.select('article > h2')[0].text.strip()
                    try:
                        item_download_link = curr_data_item.select('article span.download > a')[0]['href']
                    except IndexError as ex:
                        # occasionally breaks...
                        print(ex)
                        # so try alt DOM:
                        try:
                            item_download_link = curr_data_item.select('article span.doclink> a')[0]['href']
                        except IndexError as ex2:
                            print(f"Index Error: Failed to obtain download link: {ex2}")
                    except KeyError as ex2:
                        print(f"Key Error: Failed to obtain download link: {ex2}")

                    try:
                        _info = self.extract_item_info(curr_data_item.select('div.tab-content > div.tab-pane:nth-of-type(2)')[0].encode_contents())
                    except Exception as ex:
                        print(f"Error extracting info. {ex}")
    
                    _credits = {}
                    try:
                        _credits = self.extract_item_info(curr_data_item.select('div.tab-content > div.tab-pane:nth-of-type(3)')[0].encode_contents())
                    except Exception as ex:
                        print(f"Error extracting credits. {ex}")
    
                    topic = self.get_metadata_list_value(_info['entries'],'Palette')
    
                    # This works fine, but currently not used. leave teh method in place!
                    # # image. See https://stackoverflow.com/questions/61530606/how-to-save-pictures-from-a-website-to-a-local-folder
                    # try:
                    #     _img = self.extract_image_info(curr_data_item.select('div.tab-content > div.tab-pane:nth-of-type(1)')[0].encode_contents(),current_section,topic)
                    # except Exception as ex:
                    #     print(f"Error extracting image. {ex}")                
                    
                    try:
                        self.store_download_link(
                            {
                                'dir':os.path.join(current_section,topic,""),        # filesystem path to store in (section/topic/)
                                'filename':item_title.replace(' ','').replace('\'','').replace(',','').replace('.','').replace(':','').replace('!','')+'.zip',   # extracta meaningful zipped filename here
                                'state':'NOTFETCHED',   # 
    #                            'imagefile':_img,        # UTF8 bytestring. May not be needed
                                'info':_info,           # info metadata
                                'credits':_credits,     # credits metadata
                                'topic':topic,           # from Palette entry of info
                                'section':current_section
                             }, f"https://www.realm667.com{item_download_link}"
                            )
                    except Exception as ex:
                        print(f"Failed to store download link. {ex}")
                except ConnectionError as ex:
                    print(f"Failed to retrieve content. {ex}")

        print('done')

    def get_metadata_list_value(self,metadata_list,key):
        ''' retrieve a dict item by key '''
        return metadata_list.get(key,"xxx")

    def extract_image_info(self,bytestr,section="section",topic="topic"):
        ''' retrieve some image metadata from the passed HTML. CURRENTLY NOT USED '''
        _root =  'https://www.realm667.com'
        htmlstr = bytestr.decode('utf-8').replace('\n', ' ').replace('\r', '')
        soup = BeautifulSoup(htmlstr,'html.parser')
        img = soup.select('img')[0]
        src = img.get('src').replace('\\', '/')
        # alt = img.get('alt').replace('\\', '/')

        try:
            root_dir = os.path.realpath('')
            image_name = src.split('/')[-1]
            image_save_path = f'{root_dir}/downloads/realm667/{section}/{topic}/{image_name}'
            with urllib.request.urlopen(_root + src) as response, open(image_save_path, 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
        except Exception as ex:
            print(ex)

        return image_name

    def extract_item_info(self,bytestr):
        ''' retrieve some metadata about an item, from supplied HTML '''
        htmlstr = bytestr.decode('utf-8').replace('\n', ' ').replace('\r', '')
        _soup = BeautifulSoup(htmlstr,'html.parser')
        try:
            _title = _soup.select('h2')[0].text.strip()
        except Exception as ex:
            print(ex)
        _out = {'title':_title,'entries':{}}
        # split on BR (crappy HTML)
        _items = htmlstr.split('<strong>')
        _items.pop(0)   # remove first entry as we already have the title:
        for _item in _items:
            try:
                # split on closing strong tag:
                # if "(" in _item:
                #     breakpoint()
                
                _param = self.get_processed_category(_item)
                # _param = _item.split('</strong>')[0].replace('<br/>','')    \
                #     .replace('-','')    \
                #     .replace(':','')    \
                #     .replace(';','')    \
                #     .replace('.','')    \
                #     .replace(',','')    \
                #     .replace(' ','')    \
                #     .replace('(','')    \
                #     .replace(')','')    \
                #     .replace('[','')    \
                #     .replace(']','')    \
                #     .replace('/','_').strip().lower()
                # argh! hacky
                # if _param == 'class':
                #     _param = 'thingclass'
                _val = _item.split('</strong>')[1].replace('<br/>','').strip()
                if _param:  # account for empty param:
                    print(f"Using calculated parameter {_param}")
                    _out['entries'][_param] = _val
            except Exception as ex:
                print(ex)

        return _out
    
    def get_processed_category(self, str):
        ''' given there are a lot of spelling variations in some categories, map them to a single
         value. This collects the mappings. '''
        str.split('</strong>')[0].replace('<br/>','')    \
                    .replace('-','')    \
                    .replace(':','')    \
                    .replace(';','')    \
                    .replace('.','')    \
                    .replace(',','')    \
                    .replace(' ','')    \
                    .replace('(','')    \
                    .replace(')','')    \
                    .replace('[','')    \
                    .replace(']','')    \
                    .replace('/','_').strip().lower()
        if str == 'class':
            str = 'thingclass'
        return str
    
    category_mapper = {
        # TODO: extract logic to sort out the categories.
        # e.g. https://www.realm667.com/en/repository-18489/sfx-shoppe-mainmenu-139-58855/other-66854/1077-iwad-brightmaps#info
    }
