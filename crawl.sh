#!/bin/sh
# loop until the user presses q key
while [ "$INPUT_STRING" != "q" ]:
do
	# call fetcher.py with python alias.
	# required args:
	#
	# -d nnn.nnn.nnn.nnn
	# 
	# where nnn.nnn.nnn.nnn is the ip address of the mongoDB server
	# optional args:
	# 
	# -p nnnnn
	# -n dbstring
	# 
	# where nnnnn is mongoDB port and dbstring is the name of the mongoDB collection to use
	
	python3.6 fetcher.py -d 192.168.1.106
done

