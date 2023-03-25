import csv_reader as csvr

# file to read prices from
current_file = "new_test.txt"

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
print(str(count / key))
