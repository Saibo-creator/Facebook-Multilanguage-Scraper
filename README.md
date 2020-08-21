



Facebook Multi-Language  Scraper
===
![downloads](https://img.shields.io/github/downloads/atom/atom/total.svg)


## Table of Contents

[TOC]

## Preambule

If you are a total beginner to this, start here!

This Scraper is capable of scraping public posts in a **specific language(supports 72 languages) on Facebook**. For other social networks such as Twitter, the language can be passed as an option via its offical API, but Facebook doesn't provide with this option, where comes from the idea of making this scraper.

> I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it. [name=Bill Gates]

## Language supported
| **cmn** | **deu** | **rus**  | **fra** |
| ------- | ------- | -------- | ------- |
| **eng** | **jpn** | **spa**  | **ita** |
| **kor** | **vie** | **nld**  | **epo** |
| **por** | **tur** | **heb**  | **hun** |
| **ell** | **ind** | **ara**  | **fin** |
| **bul** | **yue** | **swe**  | **ukr** |
| **bel** | **ces** | **wuu**  | **nob** |
| **kat** | **pol** | **lat**  | **isl** |
| **afr** | **ron** | **bre**  | **tat** |
| **yid** | **uig** | **srp**  | **dan** |
| **pes** | **slk** | **eus**  | **tgl** |
| **hin** | **lit** | **ben**  | **cat** |
| **hrv** | **tha** | **mkd**  | **glg** |
| **vol** | **jbo** | **toki** | **ina** |
| **nds** | **tlh** | **ido**  | **oci** |
| **ile** | **aze** | **tuk**  | **kab** |
| **ber** | **cor** | **avk**  | **mar** |
| **mhr** | **lfn** | **run**  | **gos** |

*cmn is mandarin chinese


## Installation
1. You need to have Google Chrome bowser installed, if not please do it first as follows.

```gherkin=
#Mac
brew cask install google-chrome
#Ubuntu
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```
2. Depending on your version of Chrome, you need to download the correponding [chromedriver](https://chromedriver.chromium.org/downloads) and put it into this repo.

3. Install packages from ```requirements.txt```
```gherkin=
pip install -r requirements.txt
```
4. Install language specifique package 
```gherkin=
#for chinese, cantonese and wu ['cmn','yue','wuu']
pip install jieba
#for thai
pip install pythainlp

```


Usage
---

```gherkin=
bash ./main. afr # here I took afrikaans as example
```
- Scraped text data will be saved in `./data/page_data`
- The total scraping time in my experienment is **30MB/h**. It depends on your internet environment, also depends on the language because some languages have less users than others.

## Appendix and FAQ

:::info
**Find this document incomplete?** Leave a comment!
:::

###### tags: `Scraper` `Facebook`