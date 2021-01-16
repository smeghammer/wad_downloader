#!/bin/sh
# loop until the user presses q key
while [ "$INPUT_STRING" != "q" ]:
do
	# call fetcher.py with python alias.
	# required args:
	#
	# -s startpos
	# -d nnn.nnn.nnn.nnn
	# 
	# where nnn.nnn.nnn.nnn is the ip address of the mongoDB server and startpos is teh location to staret the crawl
	# optional args:
	# 
	# -p nnnnn
	# -n dbstring
	# 
	# where nnnnn is mongoDB port and dbstring is the name of the mongoDB collection to use
	
	python3.6 fetcher.py -d 192.168.1.106 -s 6
done

