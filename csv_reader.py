import csv

# list of vinyls as csv file
csv_filename = "vinyls - Sheet1-5.csv"

# dictionary that holds dictionaries of each vinyl
rows = {}
# reads each row in csv
with open(csv_filename, 'r') as file:
    csvreader = csv.reader(file)
    # header = next(csvreader)
    for row in csvreader:
        # creates dictionary entry
        new_dic = {
            "num": row[0],
            "title1": row[1],
            "title2": row[2],
            "artist": row[3],
            "man_price": 0,  # float(row[4]),
            "upd_price": 0
        }
        # adds dictionary into rows under number
        rows.update({int(row[0]): new_dic})

