'''
Created on 9 Jan 2021

@author: smegh
'''
import json
import requests
from libs.sqlite_database import ServerDatabaseActions
from libs.abstractcrawler import AbstractCrawler


class DWMetadataCrawler(AbstractCrawler):
    '''
    Crawl the DW API as the WAD harvester, but collect metadata into a database for subsequent
    sorting later on. triggered by a DW thread asking about numbers of maps per author
    '''
    # DB_NAME = "idgames_metadata"

    def __init__(self,*args, **kwargs):
        self.data = None
        ''' I want to have an instance od SQLite3 HERE, but not for the pother
        crawlers. So override the init() method to also initialise a SQLite3
        instance 
        
        see:
        https://stackoverflow.com/questions/12701206/how-to-extend-python-class-init
        '''
        print('metadata init...',args)
        super().__init__(*args, **kwargs)

        # and initialise the SQLite3 class:
        self.db = ServerDatabaseActions(self.metadatadb)

    def open(self):
        ''' load the URL and - for the case of JSON, load it as a dict. '''
        response = requests.get(self.url,timeout=50)
        self.data = json.loads(response.content)

        # Once the data is loaded to the class instance, call the recursive function:
        self.crawl()

    def crawl(self):
        ''' Recursive function to parse the loaded JSON and store WAD data for subsequent download '''
        print('Doomworld crawling...')

        # We know the JSON structure for ID Games API, so test for either files or directories
        # (pretty sure there are no dirs that list dub-dirs AND files but this sould handle that anyway): '''
        if 'dir' in self.data['content'] and self.data['content']['dir']:
            for item in self.data['content']['dir']:
                print(item['id'])

                # recursively instantiate the crawler with each new directory URL:
                _crawler = DWMetadataCrawler(str(item['id']),self.crawlroot,self.download_root,self.db, self.crawler_id,None,self.metadatadb)
                _crawler.open()
        if 'file' in self.data['content'] and self.data['content']['file']:
            # 'file'may be an array of file data entries OR if only one, may be just a single entry.
            # TODO: This might be an issue for the downloader too

            # if type(self.data['content']['file']) is dict:
            if isinstance(self.data['content']['file'], dict):
                print('its a dict')
                self.db.insert_idgames_data(self.data['content']['file']['id'],
                                     self.data['content']['file']['title'],
                                     self.data['content']['file']['author'],
                                     self.data['content']['file']['age'])
            # if type(self.data['content']['file']) is list:
            if isinstance(self.data['content']['file'],list):
                print('its a list')
                for item in self.data['content']['file']:

                    # Here, I need to grab the metadata, rather than download the file, and insert (or update) that into
                    # a SQLite3 instance. Once I have a relational table, I can further determine extra infor from that
                    # metadata.
                    # We have a file listing, so process it (into SQLite3) for subsequent metadata processing.
                    # Matybe a relational database, FKed on USER??:
                    # hah! nice. The 'age' field is a UNIX datestamp...
                    try:
                        print(
                            item['id'],
                            item['title'],
                            item['age'],
                            item['author'])
                        self.db.insert_idgames_data(item['id'],item['title'],item['author'],item['age'])
                    except UnicodeEncodeError as err:
                        print(f"UnicodeEncodeError error with {item['id']}, '{err}' thrown")
                    except TypeError as err:
                        print(f"TypeError with {item}, '{err}' thrown")
                    except Exception as ex:
                        print(ex)
