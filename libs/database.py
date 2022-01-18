'''
Created on 10 Jan 2021

@author: smegh
'''
import requests
import urllib.request
from pymongo import MongoClient
from pathlib import Path            #see https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
import config.sources
from random import randint
from config.sources import userAgents, crawlerData


class MongoConnection(object):
    

    '''
    classdocs
    '''
    def __init__(self, mongoIp='127.0.0.1', mongoPort=27017,databaseName='DoomWadDownloader',storeIn = 'other/'):
        '''
        Constructor
        '''
        print('instantiating database')
        self.mongoIp = mongoIp
        self.mongoPort = mongoPort
        self.downloadBase = 'downloads/'
        self.downloadPath = storeIn             #frpm dowloader initialisation
        self.ualist = userAgents
        
        #self.db = MongoClient(host=dbServer,port=dbPort)[treecreeperDBName]
        client = MongoClient(connect=False, localThresholdMS=100, host=mongoIp, port=mongoPort)
        self.db = client[databaseName]
    
    
    
            
#     def setDatabase(self,mongoIp='127.0.0.1', mongoPort=27017):

    def storeDownloadLinkObj(self,linkobj):
        try:
            if not self.isStored('downloads',linkobj['url']):
                print('storing')
                self.db['downloads'].insert_one(linkobj)
                return True
            print('already stored')
            return False
        except Exception as ex:
            print(ex)
            return False
        
    
    def getQueueItem(self,url):
        _cursor = self.db['downloads'].find({'url':url},{'_id':0});
        result = list(_cursor)
        if result:
            return(result)
        return({'result':'no record found for '+url})
        
    '''
    have we got this link already?
    collection is 'downloads' or 'crawl'
    '''
    def isStored(self,collection,url): 
        _cursor = self.db[collection].find({'url':url},{'_id':0});
        result = list(_cursor)
        print('RESULT:',result)
        if result:
            return True
        return False
        # return(dict(self.db[collection].find({'url':url})))
    
    
     
    def fetchFile(self,crawlerId=None):
        _fetched = False
        _query = {'state':'NOTFETCHED'}
        if crawlerId:
            print(crawlerData[crawlerId])
            _query = {'state':'NOTFETCHED','source':crawlerData[crawlerId]['id']}
        _res = self.db['downloads'].find_one(_query,{'_id':0})
        if _res:
           
            
            #pull the file
            # print('trying to retrieve file ' + _res['metadata']['filename'])
            
            ''' only do this if the request is a 200 '''
            Path(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir']).mkdir(parents=True, exist_ok=True)
            #store on FS( or in gridFS?)
            #lets try requests:
            
            #http only
            try:
                print('trying with requests...')
                _index = randint(0,len(self.ualist))
                _ua = self.ualist[_index]
                _headers = {'user-agent': self.ualist[randint(0,len(self.ualist))]['useragentString']}
                r = requests.get(_res['url'],headers=_headers)
                if r.status_code == 200:
                    #flag it as locked
                    self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    with open(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'], 'wb') as outfile:
                        outfile.write(r.content)
                        _fetched = True
                else: 
                    raise Exception("Request error: " +  r.status_code)
                    
            #ftp
            except Exception as ex:
                print('requests lib failed, trying with urllib...')
                try:
                    #flag it as locked
                    self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'LOCKED'}})
                    r = urllib.request.urlretrieve(_res['url'], self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'])
                    _fetched = True
                
                except Exception as ex:
                    #flag it as failed
                    self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'ERROR'}})
                    print(ex)
                    
            
            if _fetched:
                print('fetched OK. Stored in ' + self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'])
                self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'FETCHED'}})
            else:
                self.db['downloads'].update_one({'url':_res['url']},{'$set':{'state':'FAILED'}})
        
        else:
            print('Notihng to retrieve!')
        