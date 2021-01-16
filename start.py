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

'''
capture CLI args:
'''
parser = argparse.ArgumentParser(description='Start metadata collection with startnode, db server, db port and DB name')
# Required args:
parser.add_argument( '-a', '--archive', help='archive source (D=doomworld, W=wad archive, S=sentinels playground)', required=True)
parser.add_argument( '-d', '--dbserver', help='Mongo DB server IP [string]', required=True)  

# optional args
parser.add_argument( '-p', '--dbport', help='Mongo DB port [int]', required=False, default=27017)  
parser.add_argument( '-n', '--database', help='Mongo database name [string]', required=False,default='DoomWadDownloader')
args = parser.parse_args()

'''
These blocks define a crawling target.

name - arbitrary string. The name of the source
module - the filename (without extension) tha contains the relevant concrete crawler implementation
class - the python classname to load dynamically
crawlroot - the base url from which crawl URLs are constructed
downloadroot - the base url from which download URLs are constructed
storeIn - filesystem root location for downloaded files. The trailing slash is essential.
'''
crawlerData = {
    'D':{
            'name':'Doomworld',
            'module':'doomworldcrawler',
            'class':'DoomworldCrawler',
            'startAt':6,
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            'downloadroot':'ftp://ftp.fu-berlin.de/pc/games/idgames/',
            'storeIn':'doomworld/'
        },
    'W':{
            'name':'WAD Archive',
            'module':'wadarchivecrawler',
            'class':'WADArchiveCrawler',
            'startAt':'Category/WADs/',
            'crawlroot':'https://www.wad-archive.com/',
            'downloadroot':'https://assets.wad-archive.com/wadarchive/files/',
            'storeIn':'wad-archive/'
        },
    'T':{
            'name':'Sentinels Playground',
            'module':'tspgcrawler',
            'class':'SentinelsPlaygroundCrawler',
            'startAt':'zandronum/wads.php',
            'crawlroot':'https://allfearthesentinel.net/',
            'downloadroot':'https://allfearthesentinel.net/zandronum/download.php?file=',
            'storeIn':'tspg/'
        }
    }

'''
called from __main__. Dynamically loads the configured module, based on the crawlerId. Current allowed values are:

D - Doomworld config
W - WAD Archive config
T - Sentinels Playground

Note that these will likely be extended, and perhaps abstracted to actual config files...
'''
def selectCrawler(crawlerId,db):
    print("Using crawler ", crawlerData[crawlerId])
    '''
    Here, I dynamiclly load the specified crawler class
    '''
    try:
        mod = importlib.import_module('libs.' + crawlerData[crawlerId]['module'], crawlerData[crawlerId]['class'])
        clss = getattr(mod, crawlerData[crawlerId]['class'])  
        inst = clss(str(crawlerData[args.archive]['startAt']), crawlerData[args.archive]['crawlroot'], crawlerData[args.archive]['downloadroot'],db) #pass on loglevel to scraper module
        return(inst)  #this method must exist on your class
    except Exception as err:
        return({'status' : 'error','message' : str(err)})


'''
Entry point:

'''
if __name__ == '__main__':
    print('starting crawler with ' + crawlerData[args.archive]['name'] )
    db = MongoConnection(args.dbserver,args.dbport,args.database,crawlerData[args.archive]['storeIn'])
    
    ''' Here I load a crawler based on the passed arg:  '''
    crawler = selectCrawler(str(args.archive),db)
    
    #run it:
    crawler.open()

    
