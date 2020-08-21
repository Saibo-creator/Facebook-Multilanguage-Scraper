# Facebook Multi-Language  Scraper


## Installation

### Get Chrome and Chrome driver
Choose the one for your system. Below are the instructions for linux.
Downloads for chromium available at: [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

```bash
sudo apt-get install chromium-browser
sudo apt-get install chromium-chromedriver
```

**Note**: the code assumes the chromedriver is available in the same directory or is on the PATH. You can change the `executable_path` parameter if you want another directory.



### Language Options:

Afrikaans 	Albanian 	Alemannic 
Amharic 	Arabic 	Aragonese 
Armenian 	Assamese 	Asturian 
Azerbaijani 	Bashkir 	Basque 
Bavarian 	Belarusian 	Bengali 
Bihari 	Bishnupriya Manipuri 	Bosnian 
Breton 	Bulgarian 	Burmese 
Catalan 	Cebuano 	Central Bicolano 
Chechen 	Chinese 	Chuvash 
Corsican 	Croatian 	Czech 
Danish 	Divehi 	Dutch 
Eastern Punjabi 	Egyptian Arabic 	Emilian-Romagnol 
English 	Erzya 	Esperanto 
Estonian 	Fiji Hindi 	Finnish 
French 	Galician 	Georgian 
German 	Goan Konkani 	Greek 
Gujarati 	Haitian 	Hebrew 
Hill Mari 	Hindi 	Hungarian 
Icelandic 	Ido 	Ilokano 
Indonesian 	Interlingua 	Irish 
Italian 	Japanese 	Javanese 
Kannada 	Kapampangan 	Kazakh 
Khmer 	Kirghiz 	Korean 
Kurdish (Kurmanji) 	Kurdish (Sorani) 	Latin 
Latvian 	Limburgish 	Lithuanian 
Lombard 	Low Saxon 	Luxembourgish 
Macedonian 	Maithili 	Malagasy 
Malay 	Malayalam 	Maltese 
Manx 	Marathi 	Mazandarani 
Meadow Mari 	Minangkabau 	Mingrelian 
Mirandese 	Mongolian 	Nahuatl 
Neapolitan 	Nepali 	Newar 
North Frisian 	Northern Sotho 	Norwegian (Bokmål) 
Norwegian (Nynorsk) 	Occitan 	Oriya 
Ossetian 	Palatinate German 	Pashto 
Persian 	Piedmontese 	Polish 
Portuguese 	Quechua 	Romanian 
Romansh 	Russian 	Sakha 
Sanskrit 	Sardinian 	Scots 
Scottish Gaelic 	Serbian 	Serbo-Croatian 
Sicilian 	Sindhi 	Sinhalese 
Slovak 	Slovenian 	Somali 
Southern Azerbaijani 	Spanish 	Sundanese 
Swahili 	Swedish 	Tagalog 
Tajik 	Tamil 	Tatar 
Telugu 	Thai 	Tibetan 
Turkish 	Turkmen 	Ukrainian 
Upper Sorbian 	Urdu 	Uyghur 
Uzbek 	Venetian 	Vietnamese 
Volapük 	Walloon 	Waray 
Welsh 	West Flemish 	West Frisian 
Western Punjabi 	Yiddish 	Yoruba 
Zazaki 	Zeelandic 


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
