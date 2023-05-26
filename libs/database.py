'''
Created on 10 Jan 2021

@author: smegh
'''
from random import randint
#see https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
from pathlib import Path
import urllib.request
import requests
from requests.exceptions import HTTPError
from pymongo import MongoClient
from config.sources import userAgents, crawlerData


class MongoConnection():

    '''
    connect to database and wrap methods
    '''
    def __init__(self, mongo_ip='127.0.0.1', mongo_port=27017,database_name='DoomWadDownloader',storeIn = 'other/'):
        '''
        Constructor
        '''
        print('instantiating database')
        #self.mongo_ip = mongo_ip
        #self.mongoPort = mongo_port
        self.downloadBase = 'downloads/'
        #frpm dowloader initialisation
        self.downloadPath = storeIn
        self.ualist = userAgents

        #self.db = MongoClient(host=dbServer,port=dbPort)[treecreeperDBName]
        #client = MongoClient(connect=False, localThresholdMS=100, host=mongo_ip, port=mongo_port)
        #self.db = client[database_name]
        self.db = MongoClient(connect=False, localThresholdMS=100, host=mongo_ip, port=mongo_port)[database_name]

    def store_download_link_obj(self,linkobj):
        '''
        store a download link in the queue ready for fetching
        '''
        if not self.is_stored('downloads',linkobj['url'],linkobj['source']):
            print('storing')
            self.db['downloads'].insert_one(linkobj)
            return True
        print('already stored')
        return False

    def get_queue_item(self,url):
        '''
        retrieve a queue item by URL
        '''
        _cursor = self.db['downloads'].find({'url':url},{'_id':0})
        result = list(_cursor)
        if result:
            return result
        return {'result':'no record found for '+url}

    def is_stored(self,collection,url,source):
        '''
        have we got this link already?
        collection is 'downloads' or 'crawl'
        '''
        _cursor = self.db[collection].find({'url':url,'source':source},{'_id':0})
        result = list(_cursor)
        if result:
            return True
        return False

    def fetch_file(self,crawlerId=None):
        '''
        retrieve the binary specified in next available queue item
        '''
        _fetched = False
        _query = {'state':'NOTFETCHED'}
        if crawlerId:
            print(crawlerData[crawlerId])
            _query = {'state':'NOTFETCHED','source':crawlerData[crawlerId]['id']}
        _res = self.db['downloads'].find_one(_query,{'_id':0})
        if _res:
            try:
                Path(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir']).mkdir(parents=True, exist_ok=True)
            except OSError as err:
                # something fuked up wit hthe path (quote in author name etc.) - default to XXX
                Path(self.downloadBase + _res['source'] + '/xxx/').mkdir(parents=True, exist_ok=True)

            try:
                print('trying with requests...')
                # _index = randint(0,len(self.ualist)-1)
                # _ua = self.ualist[_index]
                _headers = {'user-agent': self.ualist[randint(0,len(self.ualist)-1)]['useragent']}
                r = requests.get(_res['url'],headers=_headers,timeout=45)
                if r.status_code == 200:
                    #flag it as locked
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    try:
                        with open(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'], 'wb') as outfile:
                            outfile.write(r.content)
                            _fetched = True
                    except OSError as err:
                        # bad path stored. Look at fixinfg this during th ecrawl.
                        with open(self.downloadBase + _res['source'] + '/xxx/' + _res['metadata']['filename'], 'wb') as outfile:
                            outfile.write(r.content)
                            _fetched = True
                else:
                    raise HTTPError(f"Request error: {r.status_code}")

            #ftp
            except HTTPError as ex:
                print(f'requests lib failed {ex}, trying with urllib...')
                try:
                    #flag it as locked
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    r = urllib.request.urlretrieve(_res['url'], self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'])
                    _fetched = True

                except Exception as ex2:
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'ERROR'}})
                    print(ex2)

            if _fetched:
                print('fetched OK. Stored in ' + self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'])
                res = self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'FETCHED'}})
                print(res)
            else:

                self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'FAILED'}})

        else:
            print('Notihng to retrieve!')
