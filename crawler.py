'''
Created on 9 Jan 2021

@author: smegh

TODO:
 - logging
'''
import argparse
import importlib

# from libs.doomworldcrawler import DoomworldCrawler
from libs.database import MongoConnection
from config.sources import crawlerData

'''
capture CLI args:
'''
parser = argparse.ArgumentParser(description='Start metadata collection with startnode, db server, db port and DB name')
# Required args:
parser.add_argument( '-a', '--archive', help='archive source (A, C, D, DS, DWS, S, T, W )', type=str, required=True)
parser.add_argument( '-d', '--dbserver', help='Mongo DB server IP [string]', type=str, required=False,default='127.0.0.1')
parser.add_argument( '-p', '--dbport', help='Mongo DB port [int]', required=False, type=int, default=27017)
parser.add_argument( '-n', '--database', help='Mongo database name [string]', type=str, required=False,default='DoomWadDownloader')
parser.add_argument( '-m', '--metadatadb', help='Metadata database name [string]', type=str, required=False,default='metadata.db')
args = parser.parse_args()

'''
called from __main__. Dynamically loads the configured module, based on the crawlerId. Current allowed values are:

D - Doomworld config
W - WAD Archive config
T - Sentinels Playground

Note that these will likely be extended, and perhaps abstracted to actual config files...
'''
def selectCrawler(crawlerId,db):
    '''
    Here, I dynamically load the specified crawler class
    '''
    print("Using crawler ", crawlerData[crawlerId])
    # try:
    print(crawlerData)
    print(crawlerData[crawlerId]['module'])
    print(crawlerData[crawlerId]['class'])

    mod = importlib.import_module('libs.' + crawlerData[crawlerId]['module'], crawlerData[crawlerId]['class'])
    clss = getattr(mod, crawlerData[crawlerId]['class'])
    inst = clss(
        str(crawlerData[args.archive]['startAt']),
        crawlerData[args.archive]['crawlroot'],
        crawlerData[args.archive]['downloadroot'],
        db,crawlerData[args.archive]['id'],
        1,
        args.metadatadb
        ) #pass on loglevel to scraper module
    
    print(inst)
    
    return(inst)  #this method must exist on your class
    # except Exception as err:
    #     return({'status' : 'error','message' : str(err)})

if __name__ == '__main__':
    '''
    Entry point:
    '''
    print(args.archive)
    print('starting crawler with ' + crawlerData[args.archive]['name'] )
    db = MongoConnection(args.dbserver,args.dbport,args.database,crawlerData[args.archive]['storeIn'])
    
    ''' Here I load a crawler based on the passed arg:  '''
    crawler = selectCrawler(str(args.archive),db)
    print(crawler)
    #run it:
    crawler.open()

    
