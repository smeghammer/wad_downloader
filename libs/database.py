'''
Created on 10 Jan 2021

@author: smegh
'''
from random import randint
from pathlib import Path            #see https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
import urllib.request
import requests
from requests.exceptions import HTTPError
from pymongo import MongoClient
# import config.sources
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
        self.mongoIp = mongo_ip
        self.mongoPort = mongo_port
        self.downloadBase = 'downloads/'
        self.downloadPath = storeIn             #frpm dowloader initialisation
        self.ualist = userAgents

        #self.db = MongoClient(host=dbServer,port=dbPort)[treecreeperDBName]
        client = MongoClient(connect=False, localThresholdMS=100, host=mongo_ip, port=mongo_port)
        self.db = client[database_name]

    def store_download_link_obj(self,linkobj):
        '''
        store a download link in the queue ready for fetching
        '''
        # try:
        if not self.is_stored('downloads',linkobj['url']):
            print('storing')
            self.db['downloads'].insert_one(linkobj)
            return True
        print('already stored')
        return False
        # except Exception as ex:
        #     print(ex)
        #     return False

    def get_queue_item(self,url):
        '''
        retrieve a queue item by URL
        '''
        _cursor = self.db['downloads'].find({'url':url},{'_id':0})
        result = list(_cursor)
        if result:
            return result
        return {'result':'no record found for '+url}

    def is_stored(self,collection,url):
        '''
        have we got this link already?
        collection is 'downloads' or 'crawl'
        '''
        _cursor = self.db[collection].find({'url':url},{'_id':0})
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
            Path(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir']).mkdir(parents=True, exist_ok=True)

            try:
                print('trying with requests...')
                _index = randint(0,len(self.ualist))
                _ua = self.ualist[_index]
                _headers = {'user-agent': self.ualist[randint(0,len(self.ualist))]['useragentString']}
                r = requests.get(_res['url'],headers=_headers,timeout=45)
                if r.status_code == 200:
                    #flag it as locked
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    with open(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'], 'wb') as outfile:
                        outfile.write(r.content)
                        _fetched = True
                else:
                    raise HTTPError("Request error: " +  r.status_code)

            #ftp
            except Exception as ex:
                print('requests lib failed, trying with urllib...')
                try:
                    #flag it as locked
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    r = urllib.request.urlretrieve(_res['url'], self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'])
                    _fetched = True

                except Exception as ex2:
                    #flag it as failed
# <<<<<<< HEAD
#                     self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'ERROR'}})
#                     print(ex2)

# =======
                    self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'ERROR'}})
                    print(ex2)
                    
            
# >>>>>>> branch 'master' of https://github.com/smeghammer/wad_downloader.git
            if _fetched:
                print('fetched OK. Stored in ' + self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'])
                res = self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'FETCHED'}})
                print(res)
            else:
# <<<<<<< HEAD
#                 self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'FAILED'}})

# =======
                self.db['downloads'].update_many({'url':_res['url']},{'$set':{'state':'FAILED'}})
        
# >>>>>>> branch 'master' of https://github.com/smeghammer/wad_downloader.git
        else:
            print('Notihng to retrieve!')
