'''
Created on 9 Jan 2021

@author: smegh

TODO:
 - logging
'''
import argparse
from libs.database import MongoConnection

'''
capture CLI args:
'''
parser = argparse.ArgumentParser(description='Start  server, port and DB server')
parser.add_argument( '-d', '--dbserver', help='DB server IP [string]', required=True)  
parser.add_argument( '-p', '--dbport', help='DB port [int]', required=False, default=27017)  
parser.add_argument( '-n', '--database', help='DB name [string]', required=False,default='DoomWadDownloader')
args = parser.parse_args()

if __name__ == '__main__':

    db = MongoConnection(args.dbserver,args.dbport,args.database)
    db.fetchFile()
