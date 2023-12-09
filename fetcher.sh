#!/bin/sh
# call fetcher.py with python alias.
# required args:
#
# -d nnn.nnn.nnn.nnn
# 
# where nnn.nnn.nnn.nnn is the ip address of the mongoDB server
# optional args:
# 
# -p nnnnn alternate database port
# -n dbstring for alternate database collection name
# 
# where nnnnn is mongoDB port and dbstring is the name of the mongoDB collection to use

if [ $# -lt 2 ];
	then
		echo "Please supply all positional arguments:";
		echo
		echo "./fetcher.sh \$1 \$2"
		echo
		echo "where:"
		echo "  \$1=MongoDB IP address"
		echo "  \$2=Key for download source (A, D, DS, W, T, DWS, C, R667 or DBA currently)"
		
	else
		echo $1
		echo $2

		DATABASEIP="$1"
		DOWNLOADSOURCE="$2"

		# loop until the user presses ctrl+c

		while true
		do
			python3 fetcher.py -d ${DATABASEIP} -c ${DOWNLOADSOURCE}
		done
fi



