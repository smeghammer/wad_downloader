'''
Created on 10 Jan 2021

@author: smegh
'''
import urllib.request
from pymongo import MongoClient
from pathlib import Path            #see https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory



class MongoConnection(object):
    

    '''
    classdocs
    '''


    def __init__(self, mongoIp='127.0.0.1', mongoPort=27017,databaseName='DoomWadDownloader'):
        '''
        Constructor
        '''
        print('instantiating database')
        self.mongoIp = mongoIp
        self.mongoPort = mongoPort
        
        #self.db = MongoClient(host=dbServer,port=dbPort)[treecreeperDBName]
        client = MongoClient(connect=False, localThresholdMS=100, host=mongoIp, port=mongoPort)
        self.db = client[databaseName]
    
            
#     def setDatabase(self,mongoIp='127.0.0.1', mongoPort=27017):

    def storeDownloadLinkObj(self,linkobj):
        if not self.isStored('downloads',linkobj['url']):
            print('storing')
            self.db['downloads'].insert(linkobj)
            return True
        print('already stored')
        return False
       
        
    '''
    have we got this link already?
    collection is 'downloads' or 'crawl'
    '''
    def isStored(self,collection,url): 
        return(self.db[collection].find({'url':url}).count())
    
    
    
    def fetchFile(self):
        
        _res = self.db['downloads'].find_one({'state':'NOTFETCHED'},{'_id':0})
        
        #flag it as locked
        _status = self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'LOCKED'}})
        
        #pull the file
        try: 
            print('retrieving file ' + _res['metadata']['filename'])
            Path(_res['metadata']['dir']).mkdir(parents=True, exist_ok=True)
            #store on FS( or in gridFS?)
            res = urllib.request.urlretrieve(_res['url'], _res['metadata']['dir']+_res['metadata']['filename'])
            self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'FETCHED'}})
            
        except Exception as ex:
            print(ex)
            self.db['downloads'].update({'url':_res['url']},{'$set':{'state':'FAILED'}})
        
        
        
        