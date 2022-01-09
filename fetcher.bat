@echo off
rem ARGUMENTS:
rem -d	the IP address of your mongo database server
rem optionally, you can use
rem -p nnnnn for a non-default port 
rem -n dbname for an alternate database name
rem make sure to use the actual name of your python3 alias!

if "%1"=="" 	(goto missingarg1)
if "%2"=="" (goto  runonearg) else (goto runtwoargs)




:missingarg1
 	echo ---------------------------------------------------
	echo -           MISSING DATABASE ARGUMENT!            -
	echo -                                                 -
	goto msg
	rem pause
	rem exit 0
	
:runonearg
	echo ---------------------------------------------------
	echo -             NO CRAWLERID SPECIFIED.             -
	echo -                                                 -
	echo - Using any available jobs....                    -   
	echo -                                                 -
	echo - When running, press CTRL+C to exit.             -
    echo ---------------------------------------------------
    pause
	:loop
		python fetcher.py -d %1
	goto loop
	exit 0
    goto done

:runtwoargs
	echo ---------------------------------------------------
	echo -             CRAWLERID IS SPECIFIED.             -
	echo -                                                 -
	echo - Using available jobs from %2....                -   
	echo -                                                 -
	echo - When running, press CTRL+C to exit.             -
    echo ---------------------------------------------------
    pause
	:loop2
		python fetcher.py -d %1 -c %2
	goto loop2
	exit 0
    goto done

:msg
	rem echo ---------------------------------------------------
	echo - Note: You need an available MongoDB database!   -
	echo - Please give database IP address and, optionally -
	echo - a 'source' filter to trigger downloads from a   -
	echo - specified source. If this flag is not used, the -
	echo - next unfetched download will be processed.      -
	echo -                                                 -
	echo - fetcher.bat [ip of mongoDB] [source]            -
	echo -                                                 -
	echo - The source flags currently include:             -
	echo -                                                 -
	echo - D = doomworks IDGames mirror                    -
	echo - W = WAD archive                                 -
	echo - T = The Sentinels Playground                    -
	echo - C = Camo Yoshi WAD list                         -
	echo - DWS = Doom WAD Station                          -
	echo - R667 = Realm 667                                -
	echo ---------------------------------------------------
	goto done

:: finally, exit the batch file
:done
echo Done
pause
rem exit 0

