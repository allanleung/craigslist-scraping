from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# basic setup

DRIVER_PATH = "~/Applications/Firefox.app"
BASE_URL = 'https://vancouver.craigslist.org/'
QUERY = 'olympus'

options = Options()
options.headless = True
options.add_argument("--window-size=1920, 1080")
driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)

def outputResults(posts):
    print(f'{len(posts)}) results containing "{QUERY}"')
    for i, post in enumerate(posts):
        titleDiv = post.find('a', class_='result-title')
        postTitle = titleDiv.get_text()
        postURL = titleDiv.get('href')
        postTimeText = post.find('time').get('datetime')
        postTime = datetime.strptime(postTimeText, '%Y-%m-%d %H:%M')
        ellapsedMinutes = (datetime.now() - postTime)

        print(f'{postTitle}:  {postURL}')


def stepThroughPages(posts, pageLink):
    driver.get(BASE_URL + pageLink)
    soup = BeautifulSoup(driver.page_soruce, 'html.parser')
    nextButton = soup.find('a', class_='next')
    posts.extend(soup.find_all('li', 'result-row'))


    if nextButton is None: return posts
    return stepThroughPages(posts, nextButton.get('href'))

totalPosts = stepThroughPages([], 'search/zip')
totalPosts = [post for post in totalPosts if QUERY in post.find('a', class_='results-title').get_text().lower()]

# print(len(totalPosts))

# for i, post in enumerate(totalPosts):
#     postTitle = post.find('a', class_='result-title').get_text()
#     postTimeText = post.find('time').get('datetime')
#
#     print(f'{i}: {postTitle}' )

outputResults(totalPosts)

driver.quit()
