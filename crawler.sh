#!/bin/sh
set +v

# call start.py with python alias.
# required args:
#
# -d nnn.nnn.nnn.nnn
# -a config to use (D, T, W are currently the only options) 

# where nnn.nnn.nnn.nnn is the ip address of the mongoDB server and startnode is 
# optional args:
# 
# -p nnnnn
# -n dbstring
# 
# where nnnnn is mongoDB port and dbstring is the name of the mongoDB collection to use


if [ $# -lt 2 ];

	then
		echo "Please supply all positional arguments:";
		echo
		echo "./crawler.sh \$1 \$2"
		echo
		echo "where:"
		echo "  \$1=IP address of mongo database"
		echo "  \$2=Download source flag (D, W, T, C, R667 or DWS currently)"
	else
		DATABASEIP="$1"
		DOWNLOADSOURCE="$2"
	
		python3 crawler.py -d ${DATABASEIP} -a ${DOWNLOADSOURCE}
fi


