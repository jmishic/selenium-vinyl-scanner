from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import csv_reader as csvr
import os


# global variables
url = 'https://discogs.com/'
dropdown_id = "ui-id-1"
no_item_price_box = './/div[@class = "noItems_1pC5c"]'
tracks_title = './/h1[@class = "title_1q3xW"]'
dropdown_ops = 'ui-menu-item'
price_id = './/span[@class = "price_2Wkos"]'
logo_id = 'discogs-logo'


def last_resort_writer(key, file):
    title1 = csvr.rows[key]["title1"]
    title2 = csvr.rows[key]["title2"]
    artist = csvr.rows[key]["artist"]
    file.write("title 1: " + title1 + "\n")
    file.write("title 2: " + title2 + "\n")
    file.write("artist: " + artist + "\n")
    file.write("url: UNKNOWN" + "\n")
    file.write("price: " + "$NONE\n")
    file.write("program found: UNKNOWN\n")
    file.write(str(key) + "\n")
    print("url: UNKNOWN")
    print("price: $NONE")
    print("current key: " + str(key))


def no_price_writer(key, file, driver):
    title1 = csvr.rows[key]["title1"]
    print("title 1: " + title1)
    title2 = csvr.rows[key]["title2"]
    print("title 2: " + title2)
    artist = csvr.rows[key]["artist"]
    print("artist: " + artist)
    get_url = driver.current_url
    # finds price on right side of screen
    driver.find_element(By.XPATH, no_item_price_box)
    tracks = driver.find_element(By.XPATH, tracks_title).text
    file.write("title 1: " + title1 + "\n")
    file.write("title 2: " + title2 + "\n")
    file.write("artist: " + artist + "\n")
    file.write("url: " + get_url + "\n")
    file.write("price: " + "$NONE\n")
    file.write("program found: " + tracks + "\n")
    file.write(str(key) + "\n")
    print("url: " + get_url)
    print("price: NONE")
    print("current key: " + str(key))
    # relocates back to main page
    logo = driver.find_element(By.ID, logo_id)
    logo.click()


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
            dropdown_options = driver.find_element(By.ID, dropdown_id)
            time.sleep(0.5)
            # clicks on first dropdown option
            items = dropdown_options.find_elements(By.CLASS_NAME, dropdown_ops)
            time.sleep(0.5)
            items[0].click()
            # adds current url to array
            get_url = driver.current_url
            # finds price on right side of screen
            price = driver.find_element(By.XPATH, price_id)
            tracks = driver.find_element(By.XPATH, tracks_title).text
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
            logo = driver.find_element(By.ID, logo_id)
            logo.click()
            key += 1
        except NoSuchElementException:
            try:
                no_price_writer(key, f, driver)
                key += 1
            except NoSuchElementException:
                last_resort_writer(key, f)
            except IndexError:
                return key
            except StaleElementReferenceException:
                return key
            except ElementNotInteractableException:
                return key
            return key
        except IndexError:
            return key
        except StaleElementReferenceException:
            return key
        except ElementNotInteractableException:
            return key
    f.close()
    return key


def check_unknowns(file):
    f = open(file, "r")
    data = f.readlines()
    f.close()
    if len(data) != 0:
        title1 = ""
        title2 = ""
        counter = 0
        for line in data:
            l = line.split()
            if l[0] == "title1:":
                for word in l:
                    if word != "title1:":
                        title1 += word + " "
            elif l[0] == "title2:":
                for word in l:
                    if word != "title2:":
                        title2 += word + " "
            elif l[0] == "url:":
                if l[1] == "UNKNOWN":
                    driver = webdriver.Chrome()
                    driver.implicitly_wait(0.5)
                    driver.get(url)
                    try:
                        m = driver.find_element("name", "q")
                        m.send_keys(title1)
                        time.sleep(0.5)
                        m.send_keys("/")
                        time.sleep(0.5)
                        m.send_keys(title2)
                        time.sleep(3.5)
                        dropdown_options = driver.find_element(By.ID, dropdown_id)
                        time.sleep(0.5)
                        items = dropdown_options.find_elements(By.CLASS_NAME, dropdown_ops)
                        time.sleep(0.5)
                        items[0].click()
                        # adds current url to array
                        get_url = driver.current_url
                        # finds price on right side of screen
                        price = driver.find_element(By.XPATH, price_id)
                        tracks = driver.find_element(By.XPATH, tracks_title).text
                        p = price.get_attribute('innerHTML')
                        data[counter] = ("url: " + get_url + "\n")
                        data[counter + 1] = ("price: " + str(p) + "\n")
                        data[counter + 2] = ("program found: " + tracks + "\n")
                        print("url: " + get_url)
                        print("price: " + str(p))
                        print("program found: " + tracks)
                        # relocates back to main page
                        logo = driver.find_element(By.ID, logo_id)
                        logo.click()
                    except NoSuchElementException:
                        print("Oops, didn't change anything")
                    except IndexError:
                        print("Oops, didn't change anything")
                    except StaleElementReferenceException:
                        print("Oops, didn't change anything")
                    except ElementNotInteractableException:
                        print("Oops, didn't change anything")
            title1 = ""
            title2 = ""
            counter += 1
    f = open(file, "w")
    f.writelines(data)
    f.close()


def main():
    current_file = "doublechecktest.txt"
    num_vinyls = len(csvr.rows)
    counter = 0
    # while loop to handle random crashes and bugs
    # shuts down program and reruns it if error occurs
    st = time.time()
    while counter < num_vinyls:
        counter = selenium_loop(current_file)
    print("should've worked lol")
    print("checking unknowns")
    check_unknowns(current_file)
    print("should've worked lol")
    et = time.time()
    print("Total time: " + str((et-st)/60) + " minutes")


if __name__ == '__main__':
    main()
