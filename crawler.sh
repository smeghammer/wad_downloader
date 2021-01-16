#!/bin/sh

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
	
python3.6 start.py -d 192.168.1.106 -a D


