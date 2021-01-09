# wad_downloader


Framework for downloading of .WAD files from configurable sources.


TODO:
 - Abstract Base Class for generic spider. Needs:
   - findCrawlLinks()
   - findDownloadLinks()
 
 - Generic spider instance (DW API first)
   - Writes links to crawl to DB.
   - Spider will use these and flag when done
   - Use requests and bs4
   - also writes links to download .WADs
   - need to test MIME type and/or extension
 
 - ABC for downloader(?)
   - 

   I'll build this as a PIPENV eventually with python3.6, but for now, additional package requirements are pymongo (eventually), requests (for HTTP requests) and json (for JSON -> python dict()). It'll likely require bs4 later as well for web scraping.