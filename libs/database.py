'''
Created on 10 Jan 2021

@author: smegh
'''
import requests
import urllib.request
from pymongo import MongoClient
from pathlib import Path            #see https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory



class MongoConnection(object):
    

    '''
    classdocs
    '''
    def __init__(self, mongoIp='127.0.0.1', mongoPort=27017, databaseName='DoomWadDownloader',storeIn = 'other/'):
        '''
        Constructor
        '''
        print('instantiating database')
        self.mongoIp = mongoIp
        self.mongoPort = mongoPort
        self.downloadBase = 'downloads/'
        self.downloadPath = storeIn             #frpm dowloader initialisation
        
        client = MongoClient(connect=False, localThresholdMS=100, host=mongoIp, port=mongoPort)
        self.db = client[databaseName]
    
            
    def storeDownloadLinkObj(self,linkobj):
        try:
            if not self.isStored('downloads',linkobj['url']):
                print('storing')
                self.db['downloads'].insert(linkobj)
                return True
            print('already stored')
            return False
        except Exception as ex:
            print(ex)
            return False
    
    '''
    R667
    '''
    def storeRepoPageObj(self,linkobj):
        try:
            if not self.isStored('r667repopage',linkobj['url']):
                print('storing')
                self.db['r667repopage'].insert(linkobj)
                return True
            print('already stored')
            return False
        except Exception as ex:
            print(ex)
            return False
    
    
    '''
    have we got this link already?
    collection is 'downloads' or 'crawl'
    '''
    def isStored(self,collection,url): 
        return(self.db[collection].find({'url':url}).count())
    
    
    def fetchFile(self):
        _fetched = False
        
        _res = self.db['downloads'].find_one({'state':'NOTFETCHED'},{'_id':0})
        if _res:
            #flag it as locked
            self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'LOCKED'}})
            
            #pull the file
            print('trying to retrieve file ' + _res['metadata']['filename'])
            
            ''' only do this if the request is a 200 '''
            Path(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir']).mkdir(parents=True, exist_ok=True)
            #store on FS( or in gridFS?)
            #lets try requests:
            
            #http only
            try:
                print('trying with requests...')
                r = requests.get(_res['url'])
                with open(self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'], 'wb') as outfile:
                    outfile.write(r.content)
                    _fetched = True
            #ftp
            except Exception as ex:
                print('requests lib failed, trying with urllib...')
                try:
                    urllib.request.urlretrieve(_res['url'], self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'] + _res['metadata']['filename'])
                    _fetched = True
                
                except Exception as ex:
                    print(ex)
                    
            
            if _fetched:
                print('fetched OK. Stored in ' + self.downloadBase + _res['source'] + '/' + _res['metadata']['dir'])
                self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'FETCHED'}})
            else:
                self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'FAILED'}})
        
        else:
            print('Notihng to retrieve!')
        