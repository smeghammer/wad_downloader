#!/bin/sh
while [ "$INPUT_STRING" != "q" ]:
do
	python3.6 fetcher.py -d 192.168.1.106
done

