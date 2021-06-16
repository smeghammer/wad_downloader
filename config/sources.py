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
        },
    'DWS':{
            'name':'Doom WAD Station',
            'module':'dwscrawler',
            'class':'WADStationCrawler',
            'startAt':'mega/',
            'crawlroot':'http://www.doomwadstation.net/',
            'downloadroot':'http://www.doomwadstation.net/mega/',
            'storeIn':'dws/'
        },
    'R667':{
            'name':'Realm 667',
            'module':'r667crawler',
            'class':'R667Crawler',
            'startAt':'armory-mainmenu-157-97317/doom-style-mainmenu-158-94349',
            'crawlroot':'https://www.realm667.com/index.php/en/',
            'downloadroot':'https://www.realm667.com/index.php/en/',
            'storeIn':'r667/'
        }
    }
