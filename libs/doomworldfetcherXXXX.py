'''
Created on 10 Jan 2021

@author: smegh
'''
import urllib

class DoomworldFetcher(object):
    '''
    classdocs
    '''


    def __init__(self, dbconn):
        '''
        Constructor
        '''
        self.db = dbconn

        
    def fetch(self):
        print('Fetching next available file')
        self.db.fetchFile()
        
        '''
        
        '''
        #get an unfetched result:
        
        
        
        