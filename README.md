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
