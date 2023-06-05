@echo off
rem ARGUMENTS:
rem -d	the IP address of your mongo database server
rem -s	start node ID 
rem optionally, you can use
rem -p nnnnn for a non-default port 
rem -n dbname for an alternate database name
rem make sure to use the actual name of your python3 alias!

set db=%1
set src=%2

if "%db%"=="" (goto end)
if "%src%"=="" (goto end)

echo Run the crawler
python crawler.py -d %db% -a %src%

:end

echo -------------------------------------------------
echo - Note: You need an available MongoDB database! -
echo - Please give both arguments:                   -
echo -                                               -
echo - crawler.bat [ip of mongoDB] [source flag]     -
echo -                                               -
echo -                                               -
echo - The source flags currently include:           -
echo -                                               -
echo - D = doomworks IDGames mirror                  -
echo - W = WAD archive                               -
echo - T = The Sentinels Playground                  -
echo - C = Camo Yoshi WAD list                       -
echo - DWS = Doom WAD Station                        -
echo - R667 = Realm 667                              -
echo -------------------------------------------------