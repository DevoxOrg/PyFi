"""
The primary module setting up the classes of the transaction system, as well as their relevant functions.
"""
# TODO: consider a new class, timespan or some such. Holds full_dates in a 2D numpy array ordered by weeks.
# Prepend and append blank dates to the array to make sure all weeks are full.

from decimal import Decimal
import csv
import os
import pickle
import datetime
import calendar

#//////////////////////////////////// Start global variable functions and creation\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#print(os.getcwd())

if 'Statement' in os.getcwd():
    path = '../../'
else:
    path = '../'

def date_sorter(date, order=0):
    """
    A function which takes a date in a specific format (year, month, day)
    returns the year month and day in seperate strings.

    An optional second parameter indicates how the date is originally organised.
     0 (default) = YYYY/MM/DD. 1 = DD/MM/YYYY. 2 = MM/DD/YYYY.

    The symbol separating the numbers is irrelevant,
    as long as there is a character (including whitespace) separating the values.

    (str, [int]) --->  tup

    >>> date_sorter("2014/12/31")
    datetime.date(2014, 12, 31))
    >>> date_sorter("31-12-2014", 1)
    datetime.date(2014, 12, 31))
    >>> date_sorter("12.31.2014", 2)
    datetime.date(2014, 12, 31))
    """
    if order == 0:
        day = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:]))
    elif order == 1:
        day = datetime.date(int(date[6:]), int(date[3:5]), int(date[:2]))
    elif order == 2:
        day = datetime.date(int(date[6:]), int(date[:2]), int(date[3:5]))
    else:
        print(
            'Illegal parameter\n\nParameter 2 (order): {0} is an unspecified value.\n\n'.format(str(order))
            + 'Value must be between 0-2.\n\nNone returned.')
        day = None
    return day


def date_cleaner(date_list):
    """
    A function which cleans out the datelist to hold every day 
    between the two days regardless of whether it exists within the file.

    (lst) ---> lst

    >>>date_cleaner([datetime.date(2014, 3, 24), datetime.date(2014, 3, 20)])
    [datetime.date(2014, 3, 20), datetime.date(2014, 3, 21), datetime.date(2014, 3, 22), datetime.date(2014, 3, 23), datetime.date(2014, 3, 24)]
    """
    
    new_dates = []

    date_difference = date_list[0] - date_list[len(date_list)-1]

    for day in range(date_difference.days+1):
        new_dates.append(date_list[len(date_list)-1]+datetime.timedelta(days=day))

    return new_dates


class QifItem:
    def __init__(self, qif):
        self.order = {'num': None, 'payee': None, 'amountInSplit': None, 'memoInSplit': None, 'memo': None,
                      'date': None, 'category': None, 'amount': None, 'cleared': None, 'address': None,
                      'categoryInSplit': None}
        for part in qif:
            if len(part) > 0:
                if part[0] == "!":
                    pass
                elif part[0] == "D":
                    date = part[1:]
                    date_parts = date.split("/")
                    if len(date_parts[0]) == 1:
                        date_parts[0] = "0" + date_parts[0]
                    if len(date_parts[1]) == 1:
                        date_parts[1] = "0" + date_parts[1]
                    self.order["date"] = datetime.date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                    self.textdate = date_parts[2] + "-" + date_parts[1] + "-" + date_parts[0]
                elif part[0] == "T":
                    self.order["amount"] = part[1:]
                elif part[0] == "C":
                    self.order["cleared"] = part[1:]
                elif part[0] == "P":
                    self.order["payee"] = part[1:]
                elif part[0] == "M":
                    self.order["memo"] = part[1:]
                elif part[0] == "A":
                    self.order["address"] = part[1:]
                elif part[0] == "L":
                    self.order["category"] = part[1:]
                elif part[0] == "S":
                    try:
                        self.order["categoryInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["categoryInSplit"] = [part[1:]]
                elif part[0] == "E":
                    try:
                        self.order["memoInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["memoInSplit"] = [part[1:]]
                elif part[0] == "$":
                    try:
                        self.order["amountInSplit"].append(";" + part[1:])
                    except AttributeError:
                        self.order["amountInSplit"] = [part[1:]]
                else:
                    pass

    def __repr__(self):
        keys = [thingy for thingy in self.order.keys() if thingy not in ["memoInSplit",
                                                                         "categoryInSplit",
                                                                         "amountInSplit"]]
        items = []
        for key in keys:
            items.append(self.order[key])

        keys = str(keys)
        keys.rstrip("]")
        keys.lstrip("[")
        items = str(items)
        items.rstrip("]")
        items.lstrip("[")
        return keys + "\n" + items


def make_qifs(filepath):
    qifs = []
    qif_count = 0
    with open(filepath, "r") as qif_file:
        readin = qif_file.read()
        readin.rstrip("\n")
        readin.rstrip("^")
        splitqifs = readin.split("^")
        if len(splitqifs[-1]) < 5:
            del splitqifs[-1]
        for qif in splitqifs:
            qif_count += 1
            qifs.append(QifItem(qif.split("\n")))

    return qifs

