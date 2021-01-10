'''
Created on 9 Jan 2021

@author: smegh
'''
import argparse

from libs.doomworldcrawler import DoomworldCrawler
# from pymongo import MongoClient
from libs.database import MongoConnection

'''
capture CLI args:
'''
parser = argparse.ArgumentParser(description='Start rankings scraper with server, port and DB server')
parser.add_argument( '-s', '--startnode', help='DB server IP [string]', required=True)
parser.add_argument( '-d', '--dbserver', help='DB server IP [string]', required=True)  
parser.add_argument( '-p', '--dbport', help='DB port [int]', required=False, default=27017)  
parser.add_argument( '-n', '--database', help='DB name [string]', required=False,default='DoomWadDownloader')
args = parser.parse_args()

if __name__ == '__main__':
    print('starting spider with ' + str(args.dbserver))

    #start at the /levels directory (id=6)
    apiroot = 'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id='
    downloadroot = 'ftp://ftp.fu-berlin.de/pc/games/idgames/'
    startnode = args.startnode
    db = MongoConnection(args.dbserver,args.dbport,args.database)
    
    crawler = DoomworldCrawler(apiroot + str(startnode), apiroot,downloadroot,db)
    crawler.open()

    