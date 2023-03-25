from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import csv

from selenium.common.exceptions import NoSuchElementException

url = "https://discogs.com/"
csv_filename = "vinyls - Sheet1-2.csv"

rows = {}
with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    # header = next(csvreader)
    for row in csvreader:
        new_dic = {
            "num": row[0],
            "title1": row[1],
            "title2": row[2],
            "artist": row[3],
            "man_price": row[4],
            "upd_price": row[5]
        }
        rows.update({int(row[0]): new_dic})

driver = webdriver.Chrome()
driver.implicitly_wait(0.5)

driver.get(url)
# m = driver.find_element("name", "q")

discogs_urls = []
# Searches each CD in discogs
for key in rows:
    m = driver.find_element("name", "q")
    title1 = rows[key]["title1"]
    print("title 1: " + title1)
    title2 = rows[key]["title2"]
    print("title 2: " + title2)
    artist = rows[key]["artist"]
    print("artist: " + artist)
    # Uses Selenium to search for CD
    m.send_keys(title1 + "/" + title2 + " " + artist)
    time.sleep(0.2)
    # Select(driver.find_element("name", "q")).select_by_index(0)
    # m.send_keys(Keys.ENTER)
    # clicks on first option in search dropdown using the class name
    try:
        idk = driver.find_element(By.ID, "ui-id-1")
        items = idk.find_elements(By.CLASS_NAME, "ui-menu-item")
        items[0].click()
        # adds current url to array
        get_url = driver.current_url
        discogs_urls.append(get_url)
        print("url: " + get_url)
    except NoSuchElementException:
        pass
    logo = driver.find_element(By.ID, "discogs-logo")
    logo.click()

prices = []
# use BeautifulSoup to search urls and add price to array
for url in discogs_urls:
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    price = soup.find(class_='price_2wkos')
    prices.append(price)

print(prices)
