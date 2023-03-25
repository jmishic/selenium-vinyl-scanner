from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import csv_reader as csvr
import os


def selenium_loop(current_file):
    f = open(current_file, "r")
    # last line of file should be num of last vinyl read
    last_line = 0
    if os.path.getsize(current_file) != 0:
        for line in f:
            last_line = line
        print("last line: " + last_line)
    key = int(last_line) + 1
    f.close()
    f = open(current_file, "a")
    # url for discog website
    url = "https://discogs.com/"

    # creates chrome page
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)

    # opens discogs.com in chrome
    driver.get(url)
    # m = driver.find_element("name", "q")

    # Searches each CD in discogs starting at last searched vinyl
    while key <= len(csvr.rows):
        try:
            # finds search bar on main page of discogs
            m = driver.find_element("name", "q")
            # gets titles and artist from dictionary
            title1 = csvr.rows[key]["title1"]
            print("title 1: " + title1)
            title2 = csvr.rows[key]["title2"]
            print("title 2: " + title2)
            artist = csvr.rows[key]["artist"]
            print("artist: " + artist)
            # Uses searchbar to search for CD
            m.send_keys(title1)
            time.sleep(0.5)
            m.send_keys("/")
            time.sleep(0.5)
            m.send_keys(title2)
            time.sleep(3.5)
            # commented out artist for now, was causing load issue for one track
            m.send_keys(" " + artist)
            time.sleep(2)
            # Select(driver.find_element("name", "q")).select_by_index(0)
            # m.send_keys(Keys.ENTER)
            # clicks on first option in search dropdown using the class name
            # finds search dropdown options
            dropdown_options = driver.find_element(By.ID, "ui-id-1")
            time.sleep(0.5)
            # clicks on first dropdown option
            items = dropdown_options.find_elements(By.CLASS_NAME, "ui-menu-item")
            time.sleep(0.5)
            items[0].click()
            # adds current url to array
            get_url = driver.current_url
            # finds price on right side of screen
            price = driver.find_element(By.XPATH, './/span[@class = "price_2Wkos"]')
            tracks = driver.find_element(By.XPATH, './/h1[@class = "title_1q3xW"]').text
            p = price.get_attribute('innerHTML')
            f.write("title 1: " + title1 + "\n")
            f.write("title 2: " + title2 + "\n")
            f.write("artist: " + artist + "\n")
            f.write("url: " + get_url + "\n")
            f.write("price: " + str(p) + "\n")
            f.write("program found: " + tracks + "\n")
            f.write(str(key) + "\n")
            print("url: " + get_url)
            print("price: " + str(p))
            print("program found: " + tracks)
            print("current key: " + str(key))
            # relocates back to main page
            logo = driver.find_element(By.ID, "discogs-logo")
            logo.click()
            key += 1
        except NoSuchElementException:
            return key
        except IndexError:
            return key
        except StaleElementReferenceException:
            return key
        except ElementNotInteractableException:
            return key
    f.close()
    return key


def main():
    current_file = "testtesttest.txt"
    counter = selenium_loop(current_file)


if __name__ == '__main__':
    main()
