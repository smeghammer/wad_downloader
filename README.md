# wad_downloader

## Summary
Framework for downloading of .WAD files from configurable sources.


A Proof of Concept downloader for IDGames via Doomworld API written in Python 3.6. It is a decoupled architecture with a crawler that collects metadata about each download and a fetched that runs separately which collects the files and records that they have been collected. I have used a simple abstract base class model for when I add further download sources (very much like interfaces for you java and C# programmers).

## Crawler
The current concrete implementation uses the Doomworld API and the root endpoint is

`https://www.doomworld.com/idgames/api/api.php?action=getcontents&out=json&id=0`

Opening this URL in a browser will return a JSON string like so:

`{"content":{"file":null,"dir":[{"id":6,"name":"levels/"},{"id":25,"name":"utils/"},{"id":35,"name":"prefabs/"},{"id":36,"name":"combos/"},{"id":44,"name":"themes/"},{"id":51,"name":"skins/"},{"id":56,"name":"idstuff/"},{"id":58,"name":"music/"},{"id":59,"name":"graphics/"},{"id":63,"name":"deathmatch/"},{"id":69,"name":"docs/"},{"id":71,"name":"sounds/"},{"id":89,"name":"source/"},{"id":123,"name":"lmps/"},{"id":224,"name":"misc/"},{"id":304,"name":"roguestuff/"},{"id":319,"name":"historic/"}]},"meta":{"version":3}}`


which is the top level entries for the ID Games archive database. 

Note the `id=n` properies - these identify each directory and the crawler utility needs to be started with one of these IDs so it knows where to begin the crawl from. The crawler also needs to know the IP address of your MongoDB installation and, optionally, the port and database name. It will record details of each download URL found, mark it as NOTFETCHED, and will recurse down the directory tree. Thus, the recorded database entries can be used as a simple queue for the fetcher.

You can also safely interrupt the crawl and resume, and it will skip those entries already recorded.

Please see `crawler.bat` for example usage.


## Fetcher
The fetcher is a one-shot utility that gets the next available NOTFETCHED download and triggers a download and save to the local file system. WHile downloading, the database entry is marked as PENDING and once fetched, the entry in the database is marked as FETCHED. 

It will build a dierctory structure mirroring ID Games.

Note that there is a looping batch file that will run this python code indefinitely. Further, because the stored list is managed as a queue (NOTFETCHED, PENDING, FETCHED) it is possible to have multiple fetchers running concurrently using the same queue.

Likewise, you can safely interrupt the fetcher and resume, and it will not re-download anything.

See `fetcher.bat` for usage.

## Dependencies

### Python3.6 packages
Extra python packages thtat are needed:

 - json
 - requests
 - abc (may be already deployed)
 - urllib.request
 - pymongo
 - pathlib (also may be already deployed)
 

## Future
I may build this as a PIPENV eventually with python3.6, but for now, additional package requirements are pymongo, requests and json. It'll likely require bs4 later as well for web scraping.