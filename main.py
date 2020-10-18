from selenium import webdriver
import time
from datetime import datetime
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# basic setup

DRIVER_PATH = "~/Users/allanleung/Applications/Firefox.app"
BASE_URL = 'https://vancouver.craigslist.org/'
QUERY = 'olympus'

options = Options()
options.headless = True
options.add_argument("--window-size=1920, 1200")
driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)

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

for i, post in enumerate(totalPosts):
    postTitle = post.find('a', class_='result-title').get_text()
    print('{i}: {postTitle}' )

driver.quit()
