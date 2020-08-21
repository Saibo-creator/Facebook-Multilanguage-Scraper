#!/bin/sh
lang=${1}

python fb_page_collector.py -s seeding/72seeds/${lang}_5000_3gram.txt &




date_prev=None

date_now=`date -r ./data/page_links.txt`
while [ "$date_prev" != "$date_now" ]; 
do 	
	# sleep 3m
	python page_scraper.py ${lang}
	date_prev=$date_now
	date_now=`date -r ./data/page_links.txt`
done

