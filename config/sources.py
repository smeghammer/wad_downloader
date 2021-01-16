'''
Created on 16 Jan 2021

@author: smegh


These blocks define a crawling target.

name - arbitrary string. The name of the source
module - the filename (without extension) tha contains the relevant concrete crawler implementation
class - the python classname to load dynamically
startAt - the flag that should be appended to crawlRoot (below) to construct the full starting node path
crawlroot - the base url from which crawl URLs are constructed
downloadroot - the base url from which download URLs are constructed
storeIn - filesystem root location for downloaded files. The trailing slash is essential.

'''
crawlerData = {
    
    'W':{
            'name':'WAD Archive',
            'module':'wadarchivecrawler',
            'class':'WADArchiveCrawler',
            'startAt':'Category/WADs/',
            'crawlroot':'https://www.wad-archive.com/',
            'downloadroot':'https://assets.wad-archive.com/wadarchive/files/',
            'storeIn':'wad-archive/'
        },
    'D':{
            'name':'Doomworld',
            'module':'doomworldcrawler',
            'class':'DoomworldCrawler',
            'startAt':6,
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            'downloadroot':'ftp://ftp.fu-berlin.de/pc/games/idgames/',
            'storeIn':'doomworld/'
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
