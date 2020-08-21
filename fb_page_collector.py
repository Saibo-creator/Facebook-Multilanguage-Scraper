import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import credentials
from selenium.webdriver.chrome.options import Options

USERNAME = credentials.USERNAME
PASSWORD = credentials.PASSWORD



def build_query_url_for_keyword(keyword):
    tokens=keyword.split()
    keyword="%20".join(tokens)

    return '''https://www.facebook.com/search/posts/?q={}&filters=eyJycF9hdXRob3IiOiJ7XCJuYW1lXCI6XCJtZXJnZWRfcHVibGljX3Bvc3RzXCIsXCJhcmdzXCI6XCJcIn0ifQ%3D%3D'''.format(keyword)
    #und%20es%20isch


def fb_login():
    driver.get ("https://www.facebook.com")
    driver.find_element_by_id("email").send_keys("admission20182019@yahoo.com")
    driver.find_element_by_id("pass").send_keys("840671221Bosaigeng")
    driver.find_element_by_id("u_0_d").click()



def scroll_to_end(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = 2


    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    #make a last scroll
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



if __name__ == '__main__':
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seeds-filename',
                        default='seeds.txt')


    #解析参数
    args = parser.parse_args()
    # seeds_path = os.path.join('seeding', args.seeds_filename)
    seeds_path = args.seeds_filename
    

    with open(seeds_path, 'r') as file:
        seeds = file.read().splitlines()

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("no-sandbox")
    option.add_argument("--disable-gpu")
    option.add_argument("--window-size=800,600")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--headless")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    driver = webdriver.Chrome(executable_path="./chromedriver", options=option)
    fb_login()

    page_links=[]
    group_links=[]





    for seed in tqdm(seeds,desc="page_links_retreiving"):
        url = build_query_url_for_keyword(seed)

        driver.get(url)

        scroll_to_end(driver)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        total_link=len(soup.find_all('a'))
        print('total links found in the page{}'.format(total_link))


        for item in soup.find_all('a',attrs={'class':'_7gyi'}):
            link=item.get('href')
            if link.startswith('/groups/'):
                clean_link=link[8:-12]
                group_links.append(clean_link)
            else:
                clean_link=link.split('?fref')[0].split('/?ref')[0]
                if not clean_link.startswith('https://www.facebook.com/profile.php?'):
                    if not clean_link.startswith('/events/'):
                        page_links.append(clean_link)

        page_links2wite=[link+'\n' for link in page_links]
        group_links2wite=[link+'\n' for link in group_links]


        with open('data/group_links.txt','w')as group:
            group.writelines(group_links2wite)


        with open('data/page_links.txt','w')as page:
            page.writelines(page_links2wite)


