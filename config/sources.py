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
    'A':{
            'id':'api',
            'description':'handles direct insertion via API (just Chrome plugin ATM)'
        },
    'D':{
            'id':'doomworld',
            'name':'Doomworld',
            'module':'doomworldcrawler',
            'class':'DoomworldCrawler',
            'startAt':6,
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            'downloadroot':'ftp://ftp.fu-berlin.de/pc/games/idgames/',
            'storeIn':'doomworld/'
        },
    'W':{
            'id':'wad-archive',
            'name':'WAD Archive',
            'module':'wadarchivecrawler',
            'class':'WADArchiveCrawler',
            'startAt':'Category/WADs/',
            'crawlroot':'https://www.wad-archive.com/',
            'downloadroot':'https://assets.wad-archive.com/wadarchive/files/',
            'storeIn':'wad-archive/'
        },
    'T':{
            'id':'tspg',
            'name':'The Sentinels Playground',
            'module':'tspgcrawler',
            'class':'SentinelsPlaygroundCrawler',
            'startAt':'zandronum/wads.php',
            'crawlroot':'https://allfearthesentinel.net/',
            'downloadroot':'https://allfearthesentinel.net/zandronum/download.php?file=',
            'storeIn':'tspg/'
        },
    'DWS':{
            'id':'doomwadstation',
            'name':'Doom WAD Station',
            'module':'dwscrawler',
            'class':'WADStationCrawler',
            'startAt':'mega/',
            'crawlroot':'http://www.doomwadstation.net/',
            'downloadroot':'http://www.doomwadstation.net/mega/',
            'storeIn':'dws/'
        },
    
    'C':{
            'id':'camoy',
            'name':'Camoys WAD list',
            'module':'camoycrawler',
            'class':'CamoyCrawler',
            'startAt':'wads/',
            'crawlroot':'https://camoy.sdf.org/',
            'downloadroot':'https://camoy.sdf.org/wads/',
            'storeIn':'amoy/'
        },
    
    'R667':{
            'id':'realm667',
            'name':'Realm 667',
            'module':'r667crawler',
            'class':'R667Crawler',
            'startAt':'armory-mainmenu-157-97317/doom-style-mainmenu-158-94349',
            'crawlroot':'https://www.realm667.com/index.php/en/',
            'downloadroot':'https://www.realm667.com/index.php/en/',
            'storeIn':'r667/'
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
