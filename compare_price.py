import csv_reader as csvr


def compare_prices(current_file):
    """
    compares the price that was found earlier manually by me and the price that the
    program found. if the difference between the prices are greater than 25% then it
    prints out which ones need to be checked. The prices I found are also pretty old
    so the comparisons may be off
    :param current_file: file of titles artists and prices
    """
    # array of prices
    prices = []
    with open(current_file, 'r') as file:
        for line in file:
            l = line.split()
            # appends price to prices array
            if l[0] == "price:":
                prices.append(l[1])

    # number of total inaccuracies
    count = 0
    # value of dictionary key
    key = 1
    # compares prices found to prices that were found manually
    for price in prices:
        # removes dollar sign from price and converts to usable float
        if price[1:] == 'NONE' or price[1:] == 'ONE':
            # updates new price in dictionary
            csvr.rows[key].update({"upd_price": price[1:]})
            # gets old price from dictionary
            man_price = csvr.rows[key]["man_price"]
            csvr.rows[key].update({"needs_checked": True})
            print("Number " + str(key) + " needs checked, original price: " + str(man_price) + ", found price: NONE")
            count += 1
        else:
            p = float(price[1:])
            # updates new price in dictionary
            csvr.rows[key].update({"upd_price": p})
            # gets old price from dictionary
            man_price = csvr.rows[key]["man_price"]
            if man_price != 0:
                # finds difference between the two and calculates percentage
                difference = abs(man_price - p)
                percentage = difference / man_price
                # prints out vinyls that need checked if difference is greater than 25%
                if percentage > .25:
                    # creates new value in rows dictionary
                    csvr.rows[key].update({"needs_checked": True})
                    print("Number " + str(key) + " needs checked, original price: " + str(man_price) + ", found price: " + str(p))
                    count += 1
                else:
                    csvr.rows[key].update({"needs_checked": False})
        key += 1

    print("\n" + str(count) + " need checked out of " + str(key))
    print(str(count / key) + "\n")


def check_single_titles(current_file):
    """
    Many of the vinyls are by very obscure artists and some aren't even supposed to
    be for sale (for radio only). Also only one of the two titles of the tracks was given to me.
    These two reasons lead to many of the vinyls not being on the website or the program has trouble
    finding it (because it is missing one of the titles)
    This function prints out any of the vinyls that were found to be 'UNKNOWN'
    :param current_file: file to be read from
    """
    counter = 0
    key = 0
    with open(current_file, 'r') as file:
        for line in file:
            l = line.split()
            if l[0] == "url:":
                key += 1
                if l[1] == "UNKNOWN":
                    counter += 1
                    artist = csvr.rows[key]["artist"]
                    title1 = csvr.rows[key]["title1"]
                    print("Key: " + str(key) + " " + title1 + " by " + artist + " was not found")
    print("\nTotal unknowns found: " + str(counter))


def main():
    # file to read prices from
    current_file = "doublechecktest.txt"
    # compares prices of first 137 vinyls that I had manually found their prices
    compare_prices(current_file)
    # checks to see which vinyls could not be found at all
    check_single_titles(current_file)


if __name__ == '__main__':
    main()
