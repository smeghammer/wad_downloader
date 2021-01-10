rem ARGUMENTS:
rem -d	the IP address of your mongo database server
rem optionally, you can use
rem -p nnnnn for a non-default port 
rem -n dbname for an alternate database name
rem make sure to use the actual name of your python3 alias!


echo "running fetcher"

:loop

	python fetcher.py -d 192.168.1.106

goto loop

