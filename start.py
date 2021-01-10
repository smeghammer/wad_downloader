'''
Created on 9 Jan 2021

@author: smegh

TODO:
 - logging
'''
import argparse

from libs.doomworldcrawler import DoomworldCrawler
from libs.database import MongoConnection

'''
capture CLI args:
'''
parser = argparse.ArgumentParser(description='Start metadata collection with startnode, db server, db port and DB name')
parser.add_argument( '-s', '--startnode', help='node ID to start crawl from [int]', required=True)
parser.add_argument( '-d', '--dbserver', help='Mongo DB server IP [string]', required=True)  
parser.add_argument( '-p', '--dbport', help='Mongo DB port [int]', required=False, default=27017)  
parser.add_argument( '-n', '--database', help='Mongo database name [string]', required=False,default='DoomWadDownloader')
args = parser.parse_args()

if __name__ == '__main__':
    print('starting crawler with ' + str(args.dbserver))

    apiroot = 'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id='
    downloadroot = 'ftp://ftp.fu-berlin.de/pc/games/idgames/'
    db = MongoConnection(args.dbserver,args.dbport,args.database)
    
    #instantiate a DoomworldCrawler:
    crawler = DoomworldCrawler(apiroot + str(args.startnode), apiroot,downloadroot,db)
    
    #run it:
    crawler.open()

    