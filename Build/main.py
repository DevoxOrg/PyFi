from Statement_Functions import *

#This just initiates everything

def start(write=True):
    """
    Function holds the bulk of the statement compiler and csv building mechanism

    An optional parameter decides if we rewrite the CSV's after updating the reference files.

    (bool) ---> CSV/Reference files
    """

    # compile the csvs, generate the transaction dictionary and a list of dates.
    transactions, date_list = date_splitter()

    # Check against previous records or that date.
    # Clean out duplicates, update the transaction dictionary and update the records of that date.
    dupli_clean(transactions, date_list)

    if write:  # are we making CSV's?
        csv_writer(True)


def csv_writer(everything, date1="Beginning", date2="End"):
    """
    A custom CSV writer to create CSV's with all the transactions between a set of dates.

    Default values ensure that all dates with a fully implemented reference system are used.

    First parameter is a bool that if True forces the whole reference directory to be sued.
    If False we refer to date1 and date2, date1 being the initial date and date2 being the final date (inclusive)
    as our frame of reference to include in the CSVs.

    (bool, str, str) ---> csv*
    """
    global numDict

    transactions = get_all(everything, date1, date2)

    dates = list(transactions.keys())
    dates.sort(reverse=True)
    dates = date_cleaner(dates)

    for date in dates:
        if date in transactions.keys():
            transactions[date] = transactions[date].transactions
        else:
            transactions[date] = []

    master = type_splitter(dates, transactions, numDict)

    writer(master, dates, numDict)
