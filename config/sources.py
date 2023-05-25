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
            'name':'API',
            'description':'handles direct insertion via API (just Chrome plugin ATM)',
            'storeIn':'API/'
        },
    'D':{
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

'''
25/05/23
[
{"percent":"14.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 Win10"},
{"percent":"14.4%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic Win10"},
{"percent":"7.6%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 macOS"},
{"percent":"6.7%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic macOS"},
{"percent":"5.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win10"},
{"percent":"4.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Win10"},
{"percent":"2.7%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 Linux"},
{"percent":"2.4%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.4 Safari\/605.1.15","system":"Safari Generic macOS"},
{"percent":"2.2%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic Linux"},
{"percent":"1.9%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.5%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Linux"},
{"percent":"1.5%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 macOS"},
{"percent":"1.3%","useragent":"Mozilla\/5.0 (Windows NT 10.0; rv:112.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.58","system":"Edge 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/109.0.0.0 Safari\/537.36","system":"Chrome 109.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/111.0.0.0 Safari\/537.36","system":"Chrome 111.0 Win10"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36 Edg\/113.0.1774.42","system":"Edge Generic Win10"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:102.0) Gecko\/20100101 Firefox\/102.0","system":"Firefox 102.0 Linux"},
{"percent":"0.9%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic macOS"},
{"percent":"0.9%","useragent":"Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Linux"},
{"percent":"0.8%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36 Edg\/113.0.1774.35","system":"Edge Generic Win10"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 OPR\/98.0.0.0","system":"Chrome 112.0 Win10"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/111.0.0.0 Safari\/537.36","system":"Chrome 111.0 macOS"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/109.0.0.0 Safari\/537.36","system":"Chrome 109.0 Win7"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Windows NT 10.0; rv:113.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Win10"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/111.0.0.0 Safari\/537.36 OPR\/97.0.0.0","system":"Chrome 111.0 Win10"},
{"percent":"0.7%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.68","system":"Edge 112.0 Win10"},
{"percent":"0.6%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.64","system":"Edge 112.0 Win10"},
{"percent":"0.6%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36 Edg\/113.0.1774.50","system":"Edge Generic Win10"},
{"percent":"0.6%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.3 Safari\/605.1.15","system":"Safari Generic macOS"},
{"percent":"0.6%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/111.0.0.0 Safari\/537.36","system":"Chrome 111.0 Linux"},
{"percent":"0.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; rv:102.0) Gecko\/20100101 Firefox\/102.0","system":"Firefox 102.0 Win10"},
{"percent":"0.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/99.0.4844.51 Safari\/537.36","system":"Chrome 99.0 Win10"},
{"percent":"0.5%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.4.1 Safari\/605.1.15","system":"Safari Generic macOS"},
{"percent":"0.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko\/20100101 Firefox\/102.0","system":"Firefox 102.0 Win10"},
{"percent":"0.4%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/108.0.0.0 Safari\/537.36","system":"Chrome 108.0 Linux"},
{"percent":"0.4%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/110.0.0.0 Safari\/537.36","system":"Chrome 110.0 Win10"},
{"percent":"0.4%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/111.0","system":"Firefox 111.0 Win10"},
{"percent":"0.4%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/114.0","system":"Firefox Generic Win10"},
{"percent":"0.3%","useragent":"Mozilla\/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 ChromeOS"},
{"percent":"0.3%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/110.0.0.0 Safari\/537.36","system":"Chrome 110.0 macOS"},
{"percent":"0.3%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.5 Safari\/605.1.15","system":"Safari Generic macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/15.6.1 Safari\/605.1.15","system":"Safari 15.6.1 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/108.0.0.0 Safari\/537.36","system":"Chrome 108.0 Win10"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/79.0.3945.88 Safari\/537.36","system":"Chrome 79.0 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.2 Safari\/605.1.15","system":"Safari 16.2 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/110.0.0.0 YaBrowser\/23.3.3.719 Yowser\/2.5 Safari\/537.36","system":"Yandex Browser Generic Win10"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:108.0) Gecko\/20100101 Firefox\/108.0","system":"Firefox 108.0 Linux"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\/20100101 Firefox\/111.0","system":"Firefox 111.0 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.1 Safari\/605.1.15","system":"Safari 16.1 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win10"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/109.0.0.0 Safari\/537.36","system":"Chrome 109.0 macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko)","system":"Apple Mail for OSX macOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.39","system":"Edge 112.0 Win10"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.48","system":"Edge 112.0 Win10"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 6.1; rv:102.0) Gecko\/20100101 Goanna\/6.0 Firefox\/102.0 PaleMoon\/32.0.0","system":"PaleMoon Generic Win7"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win7"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic ChromeOS"},
{"percent":"0.2%","useragent":"Mozilla\/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic ChromeOS"}]
'''

userAgents = [
{"percent":"14.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 Win10"},
{"percent":"14.4%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic Win10"},
{"percent":"7.6%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 macOS"},
{"percent":"6.7%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic macOS"},
{"percent":"5.5%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win10"},
{"percent":"4.2%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Win10"},
{"percent":"2.7%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36","system":"Chrome 112.0 Linux"},
{"percent":"2.4%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit\/605.1.15 (KHTML, like Gecko) Version\/16.4 Safari\/605.1.15","system":"Safari Generic macOS"},
{"percent":"2.2%","useragent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36","system":"Chrome Generic Linux"},
{"percent":"1.9%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.5%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic Linux"},
{"percent":"1.5%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 macOS"},
{"percent":"1.3%","useragent":"Mozilla\/5.0 (Windows NT 10.0; rv:112.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/112.0.0.0 Safari\/537.36 Edg\/112.0.1722.58","system":"Edge 112.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/109.0.0.0 Safari\/537.36","system":"Chrome 109.0 Win10"},
{"percent":"1.1%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/111.0.0.0 Safari\/537.36","system":"Chrome 111.0 Win10"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/113.0.0.0 Safari\/537.36 Edg\/113.0.1774.42","system":"Edge Generic Win10"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko\/20100101 Firefox\/112.0","system":"Firefox 112.0 Linux"},
{"percent":"1.0%","useragent":"Mozilla\/5.0 (X11; Linux x86_64; rv:102.0) Gecko\/20100101 Firefox\/102.0","system":"Firefox 102.0 Linux"},
{"percent":"0.9%","useragent":"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko\/20100101 Firefox\/113.0","system":"Firefox Generic macOS"},
]
