# Facebook Multi-Language  Scraper
===
![downloads](https://img.shields.io/github/downloads/atom/atom/total.svg)
![build](https://img.shields.io/appveyor/ci/:user/:repo.svg)
![chat](https://img.shields.io/discord/:serverId.svg)

## Table of Contents

[TOC]


This Scraper is capable of scraping public posts in a **specific language(supports 72 languages) on Facebook**. For other social networks such as Twitter, the language can be passed as an option via its offical API, but Facebook doesn't provide with this option. 

## Languages Supported

|**cmn**| **deu**| **rus**| **fra**|
|-----|------|------|------|
|**eng**| **jpn**| **spa**| **ita**|
|**kor**| **vie**| **nld**| **epo**|
|**por**| **tur**| **heb**| **hun**|
|**ell**| **ind**| **ara**| **fin**|
|**bul**| **yue**| **swe**| **ukr**|
|**bel**| **ces**| **wuu**| **nob**|
|**kat**| **pol**| **lat**| **isl**|
|**afr**| **ron**| **bre**| **tat**|
|**yid**| **uig**| **srp**| **dan**|
|**pes**| **slk**| **eus**| **tgl**|
|**hin**| **lit**| **ben**| **cat**|
|**hrv**| **tha**| **mkd**| **glg**|
|**vol**|**jbo** |**toki**| **ina**|
|**nds**| **tlh**| **ido**| **oci**|
|**ile**| **aze**| **tuk**| **kab**|
|**ber**| **cor**| **avk**| **mar**|
|**mhr**| **lfn**| **run**| **gos**|

*cmn is mandarin chinese

## Installation

### Get Chrome and Chrome driver
Choose the one for your system. Below are the instructions for linux.
Downloads for chromium available at: [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

```bash
sudo apt-get install chromium-browser
sudo apt-get install chromium-chromedriver
```

**Note**: the code assumes the chromedriver is available in the same directory or is on the PATH. You can change the `executable_path` parameter if you have chromedriver in another directory.






### prerequisites
```bash
sudo apt install g++
pip install facebook-scraper, nltk, jieba， mecab-python3,unidic-lite, pythainlp,

japanses:pip install spacy sudachipy sudachidict_core
```

### Create the environment and download nltk resource
```bash
conda env create --file environment.yml
python -c "import nltk; nltk.download('punkt')"
```

## Usage
### Generate seeds

```bash
python seeding/seeding.py sample_seeds -g 3 3 -n 50 -c gsw_corpus.txt
# sample_seeds:the filename of the seeds txt file -g: ngram ; -n: number of seeds to produce; gsw_corpus.txt: corpus to use 
```

### Run the scraper

```bash
source activate scraper_env
python twitter_scraper.py -s seeds_2grams_5000.txt # -s specify the seeds to use for scraping
```

You should then obtain a folder called gsw_twitter_data with the labeled data.
The code has a lot of parameters, so make use of them as you prefer.

### Notes

- if you try to run the collection again in the same folder after you ran it before, it will ask "Do you want me to delete and collect the data again? (y|N|all|allno)". `y`: yes for this hashtag, `N` no for this hashtag, `all`: yes for all hashtags, `allno`: no for all hashtags
