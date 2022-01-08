# WAD Downloader

## Summary
A python3 framework for downloading of .WAD files from configurable sources.

It is a decoupled architecture with is composed of two main parts:

 - A MongoDB database backend to hold the download metadata and queue.
 - A number of site-specific crawlers that collect metadata about each download link found. 
 - A fetcher that runs separately which checks the database for available downloads and collects the file specified file. It also records that the file has been collected. 
 
Please see comments on code for more deatils of how this works.

## Crawler
I have used an abstract base class model for the crawler (https://github.com/smeghammer/wad_downloader/blob/master/libs/abstractcrawler.py). This enforces a suitable set of methods being available for when I add further download sources (very much like interfaces for you java and C# programmers). [note: I'll probably change the interface at some point as some method stubs are redundant]

## Storage
The crawler requires access to a MongoDB database. This may be local or remote. See https://docs.mongodb.com/manual/administration/install-community/ for installation details. Note, if you wish to use a non-local database, you must configure the MongoDB server to accept connections from an IP address other than localhost (127.0.0.1). This may be done in the `mongod.conf` file, as specified in, for example, https://stackoverflow.com/questions/58323458/connecting-to-a-remote-mongodb-server. 

### Concrete crawlers
So far, there are four implementations:

 - [Doomworld API](https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=0) (JSON)
 - [WAD Archive](https://www.wad-archive.com/Category/WADs) (web scrape)
 - [The Sentinels Playground](https://allfearthesentinel.net/zandronum/wads.php) (web scrape)
 - [Doom WAD Station](http://www.doomwadstation.net/mega/) (web scrape, not SSL!)
 
#### Example
The current ID Games concrete implementation of a crawler uses the Doomworld API and the root endpoint is

`https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=0`

Opening this URL in a browser will return a JSON string like so:

`{"content":{"file":null,"dir":[{"id":6,"name":"levels/"},{"id":25,"name":"utils/"},{"id":35,"name":"prefabs/"},{"id":36,"name":"combos/"},{"id":44,"name":"themes/"},{"id":51,"name":"skins/"},{"id":56,"name":"idstuff/"},{"id":58,"name":"music/"},{"id":59,"name":"graphics/"},{"id":63,"name":"deathmatch/"},{"id":69,"name":"docs/"},{"id":71,"name":"sounds/"},{"id":89,"name":"source/"},{"id":123,"name":"lmps/"},{"id":224,"name":"misc/"},{"id":304,"name":"roguestuff/"},{"id":319,"name":"historic/"}]},"meta":{"version":3}}`

which is the top level entries for the ID Games archive database. 

Note the `id=n` properies - these identify each directory and the crawler utility needs to be started with one of these IDs so it knows where to begin the crawl from. The crawler also needs to know the IP address of your MongoDB installation and, optionally, the port and database name. It will record details of each download URL found, mark it as NOTFETCHED, and will recurse down the directory tree. Thus, the recorded database entries can be used as a simple queue for the fetcher.

You can also safely interrupt the crawl and resume, and it will skip those entries already recorded.

Please see `crawler.bat`/`crawler.sh` for example usage.


## Fetcher
The fetcher is a one-shot utility that gets the next available NOTFETCHED download and triggers a download and save to the local file system of whatever is specified in the download link. WHile downloading, the database entry is marked as PENDING and once fetched, the entry in the database is marked as FETCHED. Therefore, you can use the database as a download queue. 

It will build a directory structure mirroring ID Games.

Note that there is a looping batch file that will run this python code indefinitely. Further, because the stored list is managed as a queue (NOTFETCHED, PENDING, FETCHED) it is possible to have multiple fetchers running concurrently using the same queue.

Likewise, you can safely interrupt the fetcher and resume, and it will not re-download anything (unless you clear the DB of course).

See `fetcher.bat`/`fetcher.sh` for example usage.

## Dependencies

### Python3.6 packages
Extra python packages that are needed:

 - json
 - requests
 - abc (may be already deployed)
 - bs4 (BeautifulSoup)
 - urllib.request
 - pymongo
 - pathlib (also may be already deployed)
 - lxml (html scraping)
 

## Future
I may build this as a PIPENV eventually with python3.8, but for now, additional package requirements are as listed above.
