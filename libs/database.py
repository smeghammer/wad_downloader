'''
Created on 10 Jan 2021

@author: smegh
'''
from pymongo import MongoClient
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
        
        