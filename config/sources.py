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

userAgents = [
    {"useragentString":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","useragentType":"Chrome 96.0"}, 
    {"useragentString":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0","useragentType":"Firefox 95.0"},  
    {"useragentString":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","useragentType":"Chrome 96.0"},  
    {"useragentString":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36","useragentType":"Chrome 96.0"},  
    {"useragentString":"Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0","useragentType":"Firefox 91.0"},  
    {"useragentString":"Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0","useragentType":"Firefox 95.0"},  
    {"useragentString":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36","useragentType":"Chrome 96.0"},  
    {"useragentString":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0","useragentType":"Firefox 95.0"},  
    {"useragentString":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36","useragentType":"Chrome 96.0"}
]
