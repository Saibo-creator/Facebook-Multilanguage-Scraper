from facebook_scraper import get_posts
import facebook_scraper as fbs
import concurrent.futures
import os
import sys
import fasttext as ft
import pandas as pd


def scrape_page(name,lang, page_limit=None):
    df=pd.DataFrame(fbs.get_posts(name, page_limit=page_limit)) 
    page_posts_df=df[['text']].dropna()

    #split into sentences
    page_posts_df['sentence']=page_posts_df['text'].apply(lambda x:x.split('\n'))
    page_posts_df=page_posts_df.explode('sentence')

    # langauge identification
    page_posts_df['pred']=page_posts_df['sentence'].apply(lambda x:lid.predict(x)[0][0])
    page_posts_df['proba']=page_posts_df['sentence'].apply(lambda x:lid.predict(x)[1][0])
    page_posts_df['pred']=page_posts_df['pred'].apply(lambda x: x[-3:])

    # remove empty sentences such as ".",""
    page_posts_df=page_posts_df[page_posts_df['sentence'].apply(len)>=3]
    page_posts_df.dropna(subset=['sentence'],inplace=True)

    page_posts_gsw_df=page_posts_df[(page_posts_df['pred']==lang)&(0.9<=page_posts_df['proba'])]

    # count the number of tokens of each sentence
    if lang not in ['cmn','yue','wuu','jpn','tha']:
        page_posts_gsw_df['tokens_num']=page_posts_gsw_df['sentence'].apply(lambda x: len(x.split()))
        page_posts_gsw_df=page_posts_gsw_df[(page_posts_gsw_df['tokens_num']>=3)]


    # remove emoji
    page_posts_gsw_df['sentence']=page_posts_gsw_df['sentence'].apply(remove_emoji)

    # remove extra ponctuations
    page_posts_gsw_df['sentence']=page_posts_gsw_df['sentence'].apply(lambda x:x.strip('.'))

    # drop duplicates
    page_posts_gsw_df=page_posts_gsw_df.drop_duplicates('sentence')

    filename = 'data/page_data/'+str(name) + "_posts.csv"
    fbs.write_posts_to_csv(name, page_limit=page_limit,filename=filename)

    page_posts_gsw_df['sentence'].to_csv(filename,index=False,header=False)

    print('finished scraping page : ', name)


def clear_previous_data_if_exists(dirname):
    print('data already exists, so collection has been launched before')
    print('The scraper will keep the data already fetched and continue only with new pages links')

    # s is the answer for skip
    return 's'

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('langauge', help='extra info to name the saved file')


    args = parser.parse_args()

    # Read pages name 
    with open('./data/page_links.txt','r') as file:
        pages = file.read().splitlines() # to get rid of \n 
    page_names=[link[25:] for link in pages]

    data_folder_name='./data/page_data/'

    if not os.path.exists(data_folder_name):
        os.makedirs(data_folder_name)

    if os.listdir(data_folder_name):
        mode=clear_previous_data_if_exists(data_folder_name)
    else:
        # if the dir data is empty, then this is a brand new scrape, we consider it as override
        mode='o'
    if mode=='s':
        existing_files=[fn[:-10] for fn in os.listdir(data_folder_name)]
        page_names= [name for name in page_names if name not in existing_files]


    lid = ft.load_model("./seeding/src/langdetect72.ftz")
    # scrape pages one by one

    os.chdir(data_folder_name)

    for page in page_names:
        try:
            # with concurrent.futures.ProcessPoolExecutor() as executor:
            #     executor.map(scrape_page, page_names)
                scrape_page(page,args.langauge)
        except Exception as e:
            # print("Exception: {}".format(e))
            pass





    


