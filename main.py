from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
import csv_reader as csvr
import os


# global variables
# discogs url
url = 'https://discogs.com/'
# id for search bar dropdown
dropdown_id = "ui-id-1"
# xpath for box that appears when no price is shown for item
no_item_price_box = './/div[@class = "noItems_1pC5c"]'
# xpath to title displaying artist and tracks on page
tracks_title = './/h1[@class = "title_1q3xW"]'
# list of dropdown options for search bar
dropdown_ops = 'ui-menu-item'
# xpath to price listing on page
price_id = './/span[@class = "price_2Wkos"]'
# id for logo
logo_id = 'discogs-logo'


def last_resort_writer(key, file):
    """
    function gets called if selenium is unable to find the page of a vinyl
    writes unknown values into the text file for url, price, and program found
    :param key: key for track currently searching up
    :param file: file to be written to
    """
    # grabs titles and artist from csv file
    title1 = csvr.rows[key]["title1"]
    title2 = csvr.rows[key]["title2"]
    artist = csvr.rows[key]["artist"]
    # writes information to file
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
    """
    function that gets called when a vinyl has no current listed price
    writes info to current file with normal info just replacing price with $NONE
    :param key: key for track currently searching up
    :param file: file to be written to
    :param driver: chrome webdriver selenium is using
    """
    # gets titles and artist from csv file
    title1 = csvr.rows[key]["title1"]
    print("title 1: " + title1)
    title2 = csvr.rows[key]["title2"]
    print("title 2: " + title2)
    artist = csvr.rows[key]["artist"]
    print("artist: " + artist)
    # grabs url of the page found
    get_url = driver.current_url
    # finds price on right side of screen
    driver.find_element(By.XPATH, no_item_price_box)
    # finds title on page (artist - track 1 / track2)
    tracks = driver.find_element(By.XPATH, tracks_title).text
    # writes info to file
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
    """
    main selenium loop that continues searching up vinyls and records
    data into a text file. Has exceptions to handle various crashes to
    keep the loop running. Program starts searching from the last key in
    the given text file so program doesn't completely start over when it crashes
    :param current_file: file to be read and written to
    """

    f = open(current_file, "r")

    # last line of file should be num of last vinyl read
    last_line = 0

    # finds current key to begin search on
    if os.path.getsize(current_file) != 0:
        for line in f:
            last_line = line
        print("last line: " + last_line)
    key = int(last_line) + 1
    f.close()

    # opens file to append to
    f = open(current_file, "a")

    # creates chrome page
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)

    # opens discogs.com in chrome
    driver.get(url)

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

            # Uses searchbar to search for vinyl
            if title2 == "":
                m.send_keys("45 rpm vinyl")
                time.sleep(1.5)
                m.send_keys(" " + artist)
                time.sleep(2)
                m.send_keys(" " + title1)
                time.sleep(2)
            else:
                m.send_keys(title1)
                time.sleep(0.5)
                m.send_keys("/")
                time.sleep(0.5)
                m.send_keys(title2)
                time.sleep(3.5)
                m.send_keys(" " + artist)
                time.sleep(2)

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

            # finds vinyl title (artist - track1 / track2)
            tracks = driver.find_element(By.XPATH, tracks_title).text

            # gets text of price found before
            p = price.get_attribute('innerHTML')

            # writes information to file
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

        # if item is not found on page due to invalid search
        except NoSuchElementException:
            try:
                # checks to see if just the price was missing
                no_price_writer(key, f, driver)
                key += 1
            # if vinyl wasn't found by program, inserts blank info to file
            except NoSuchElementException:
                last_resort_writer(key, f)
            # all other excepts are just selenium faults and resetting program fizes them
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
    """
    function to double-check vinyls that were previously found as unknown
    :param file: file to be read and rewritten to
    """
    # opens file and reads line into an array
    f = open(file, "r")
    data = f.readlines()

    # prints lines in array form to check if it worked
    print(data)
    f.close()

    # performs a selenium search on titles that have unknown urls
    if len(data) != 0:
        title1 = ""
        title2 = ""
        artist = ""
        counter = 0

        # opens chrome webdriver
        driver = webdriver.Chrome()
        driver.implicitly_wait(0.5)
        driver.get(url)

        # loops through each line in data searching for titles of tracks and unknown urls
        for line in data:
            l = line.split()
            if l[0] == "title" and l[1] == "1:":
                # appends entire title to title1
                for word in l:
                    if word != "title":
                        if word != "1:":
                            title1 += word + " "
                print("title 1 found: " + title1)
            elif l[0] == "title" and l[1] == "2:":
                # appends entire title to title2
                for word in l:
                    if word != "title":
                        if word != "2:":
                            title2 += word + " "
                print("title 2 found: " + title2)
            elif l[0] == "artist:":
                # appends entire artist to artist
                for word in l:
                    if word != "artist:":
                        artist += word + " "
                print("artist found: " + artist)
            elif l[0] == "url:":
                if l[1] == "UNKNOWN":
                    try:
                        # locates search bar
                        m = driver.find_element("name", "q")
                        # sends title to search bar
                        # does not search with artist name because adding artist
                        # name is what causes some errors in the original function
                        if title2 == "":
                            m.send_keys("45 rpm vinyl ")
                            time.sleep(1)
                            m.send_keys(title1)
                            time.sleep(2)
                            m.send_keys(" " + artist)
                            time.sleep(2)
                        else:
                            m.send_keys(title1)
                            time.sleep(0.5)
                            m.send_keys("/")
                            time.sleep(0.5)
                            m.send_keys(title2)
                            time.sleep(3.5)

                        # finds dropdown in search bar
                        dropdown_options = driver.find_element(By.ID, dropdown_id)
                        time.sleep(0.5)

                        # gets list of items in the dropdown
                        items = dropdown_options.find_elements(By.CLASS_NAME, dropdown_ops)
                        time.sleep(0.5)

                        # clicks on first element in the dropdown
                        items[0].click()

                        # adds current url to array
                        get_url = driver.current_url

                        # finds price on right side of screen
                        price = driver.find_element(By.XPATH, price_id)

                        # finds title of page (artist - track1 / track2)
                        tracks = driver.find_element(By.XPATH, tracks_title).text

                        # gets price text
                        p = price.get_attribute('innerHTML')

                        # changes data array to replace UNKNOWNs with values found
                        data[counter] = ("url: " + get_url + "\n")
                        data[counter + 1] = ("price: " + str(p) + "\n")
                        data[counter + 2] = ("program found: " + tracks + "\n")
                        print("url: " + get_url)
                        print("price: " + str(p))
                        print("program found: " + tracks)

                        # relocates back to main page
                        logo = driver.find_element(By.ID, logo_id)
                        logo.click()
                    # if error still occurs, nothing changes in the text file
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
                artist = ""
            # resets titles and increases counter
            counter += 1
    # reopens file and rewrites entire thing with updated values
    f = open(file, "w")
    f.writelines(data)
    f.close()


def main():
    # file name
    current_file = "doublechecktest.txt"
    # number of total vinyls
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
    # calculates and prints total time taken
    print("Total time: " + str((et-st)/60) + " minutes")


if __name__ == '__main__':
    main()
