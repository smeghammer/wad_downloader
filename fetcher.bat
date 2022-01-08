@echo off
rem ARGUMENTS:
rem -d	the IP address of your mongo database server
rem optionally, you can use
rem -p nnnnn for a non-default port 
rem -n dbname for an alternate database name
rem make sure to use the actual name of your python3 alias!


set db=%1

if "%db%"=="" (goto end)

echo "running fetcher"

:loop

	python fetcher.py -d %db% 

goto loop

:end

echo -------------------------------------------------
echo - Note: You need an available MongoDB database! -
echo - Please give database IP address:              -
echo -                                               -
echo - fetcher.bat [ip of mongoDB]                   -
echo -                                               -
echo -------------------------------------------------


