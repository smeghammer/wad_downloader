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
    'DMC':{
        'id':'dmc',
        'name':'Doomworld API metadata collector',
        'description':'extracts metadata from the ID Games API JSON output and inserts/updates to a SQL database table',
            'module':'dwmetadatacrawler',
            'class':'DWMetadataCrawler',
            'startAt':6,    # maps root
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            'downloadroot':None,
            'storeIn':None
    },
    'A':{
            'id':'api',
            'name':'API',
            'description':'handles direct insertion via API (just Chrome plugin ATM)',
            'storeIn':'API/'
        },
    'D':{   # OK
            'id':'doomworld',
            'name':'Doomworld',
            'module':'doomworldcrawler',
            'class':'DoomworldCrawler',
            'startAt':6,
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            # 'downloadroot':'ftp://ftp.fu-berlin.de/pc/games/idgames/',
            'downloadroot' : 'https://www.quaddicted.com/files/idgames/',
            'storeIn':'doomworld/'
        },
     'DS':{
         # OK
            'id':'doomshack',
            'name':'Doomshack',
            'module':'doomshackcrawler',
            'class':'DoomShackCrawler',
            'startAt':'wadlist.php',
            'crawlroot':'https://doomshack.org/',
            'downloadroot':'https://doomshack.org',
            'storeIn':'doomshack/'
         },
    'W':{
            # No
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
            # OK
            'id':'tspg',
            'name':'The Sentinels Playground',
            'module':'tspgcrawler',
            'class':'SentinelsPlaygroundCrawler',
            'startAt':'zandronum/wads.php',
            'crawlroot':'https://allfearthesentinel.com/',
            'downloadroot':'https://allfearthesentinel.com/zandronum/download.php?file=',
            'storeIn':'tspg/'
        },
    'DWS':{
        # Fails
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
        # No
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
        # No
            'id':'realm667',
            'name':'Realm 667',
            'module':'r667crawler',
            'class':'R667Crawler',
            'startAt':'repository-18489',
            'crawlroot':'https://www.realm667.com/en/',
            'downloadroot':'https://www.realm667.com/en/',
            'storeIn':'r667/'
        },
    'DBA':{
            'id':'dba',
            'name':'Doomworld by Author',
            'module':'dbacrawler',
            'class':'DBACrawler',
            'startAt':6,
            'crawlroot':'https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=',
            'downloadroot' : 'https://www.quaddicted.com/files/idgames/',
            'storeIn':'doomworld/'
        },
    }

userAgents = [
{"percent":"14.5%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36","system":"Chrome 112.0 Win10"},
{"percent":"14.4%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36","system":"Chrome Generic Win10"},
{"percent":"7.6%","useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36","system":"Chrome 112.0 macOS"},
{"percent":"6.7%","useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36","system":"Chrome Generic macOS"},
{"percent":"5.5%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0","system":"Firefox 112.0 Win10"},
{"percent":"4.2%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0","system":"Firefox Generic Win10"},
{"percent":"2.7%","useragent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36","system":"Chrome 112.0 Linux"},
{"percent":"2.4%","useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15","system":"Safari Generic macOS"},
{"percent":"2.2%","useragent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36","system":"Chrome Generic Linux"},
{"percent":"1.9%","useragent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.5%","useragent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0","system":"Firefox Generic Linux"},
{"percent":"1.5%","useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0","system":"Firefox 112.0 macOS"},
{"percent":"1.3%","useragent":"Mozilla/5.0 (Windows NT 10.0; rv:112.0) Gecko/20100101 Firefox/112.0","system":"Firefox 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58","system":"Edge 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36","system":"Chrome 109.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","system":"Chrome 111.0 Win10"},
{"percent":"1.0%","useragent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42","system":"Edge Generic Win10"},
{"percent":"1.0%","useragent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.0%","useragent":"Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0","system":"Firefox 102.0 Linux"},
{"percent":"0.9%","useragent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0","system":"Firefox Generic macOS"},
]
