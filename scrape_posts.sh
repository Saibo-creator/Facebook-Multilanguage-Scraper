#!/bin/sh


for page_url in $(cat ./data/page_links.txt); do facebook-scraper $page_url -p 10000 ; done