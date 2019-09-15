from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import os

chrome_options = Options()
chrome_options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})

driver = webdriver.Chrome(chrome_options=chrome_options)
globalarray = []

def iterate(sites):
    driver.get("https://mobile.facebook.com")
    driver.find_element_by_name("email").send_keys(os.environ['email'])
    driver.find_element_by_name("pass").send_keys(os.environ['password'])
    driver.find_element_by_name("login").click()
    driver.back()
    driver.implicitly_wait(15)
    for site in sites:
        driver.find_element_by_name("query").send_keys(site,Keys.ENTER)
        driver.find_element_by_class_name("cf").click()
        process(driver.page_source)
    # driver.close()

def process(src):
    soup = BeautifulSoup(src, features="html.parser")
    articles = soup.find_all(attrs={'role':'article'})
    for article in articles:
        text = ''.join(t.get_text() for t in article.find_all('p'))
        if text == '':
            continue
        author = article.find('a').get_text()
        likes = article.find(class_="gm")['aria-label'].split(' ')[0]
        print(author, text, likes)


iterate(["monash love letter"])