from Statement_Classes import *

store = {}

'''
////////////////////////////////////////////Start format Standardisation Functions\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
'''

def OFX(filename, dates, organiser, account):
    global keylist
    global specials_list
    global numDict

    transactions = []

    types = list(numDict.keys())

    with open(filename, 'r') as old:

        intrans = False

        for line in old:
            line = line.lstrip()
            if intrans:
                if line.startswith('</STMTTRN>'):
                    intrans = False

                    for combo in [trans_name + trans_memo, trans_name + ' ' + trans_memo, trans_name, trans_memo]:
                        if '&amp;' in combo:
                            combo = combo.replace('&amp;', '&')
                        if combo in keylist:
                            print('found', combo)
                            use = combo
                            break
                        elif combo in specials_list:
                            use = combo
                            break
                    else:
                        use = (trans_name + ' ' + trans_memo)

                        specialness = input(use + " for " + str(newtrans["amount"]) + " on " + newtrans['date'] +
                                            " is not a recognised transaction. Is this a generic transaction" +
                                            " or part of a group of transactions? ")

                        if specialness:
                            keylist, specials_list = special_maker(use, keylist, specials_list)
                        else:
                            # Then what kind of transaction is it?

                            ktypeo = input("What type of transaction is " + use + " for " + str(newtrans[
                                "amount"]) + " on " + newtrans['date'] +
                                "? Bills, Food, Income, Gifts, Travel, Savings or Other: ")
                            # ask for the type

                            # make sure it is a valid type
                            if not ktypeo in types:
                                vals = False
                                while not vals:
                                    ktypeo = input(
                                        "That is not a valid type of transaction, please enter either{0}.".format(
                                            str(types)) + "Capitalisation is important: ")
                                    # keep asking until it is a valid type
                                    # Then it is a valid type
                                    if ktypeo in types:
                                        vals = True

                            # We now know what type of transaction it is.
                            for key in numDict.keys():
                                # so loop through the transaction types until we find the right one.
                                if ktypeo == key:
                                    #increment the number of transactions we have of this type.
                                    numDict[key] += 1
                                    #and add it to the keylist.
                                    keylist[use] = [ktypeo, numDict[key] - 1]
                    newtrans['name'] = use

                    transactions.append(Transaction(newtrans['amount'], newtrans['name'], newtrans['account_name'],
                                                    date_sorter(newtrans['date'])))
                elif line.startswith('<DTPOSTED>'):
                    newtrans['date'] = line[10:14] + '-' + line[14:16] + '-' + line[16:18]

                elif line.startswith('<TRNAMT>'):
                    if ('</TRNAMT>') in line:
                        newtrans['amount'] = line[8:len(line)-10]
                    else:
                        newtrans['amount'] = line[8:len(line)-1]

                elif line.startswith('<NAME>'):
                    if '</NAME>' in line:
                        trans_name = line[6:len(line)-8]
                    else:
                        trans_name = line[6:len(line)-1]

                elif line.startswith('<MEMO>'):
                    if '</MEMO>' in line:
                        trans_memo = line[6:len(line)-8]
                    else:
                        trans_memo = line[6:len(line)-1]

            else:
                if line.startswith('<STMTTRN>'):
                    intrans = True
                    newtrans = {'amount': None, 'name': None, 'account_name': account, 'date': None}

    for trans in transactions:
        if trans.date not in dates:
            dates.append(trans.date)
        if trans.date not in organiser:
            organiser[trans.date] = []
        organiser[trans.date].append(trans)


    key_maker(keylist, specials_list)

    return organiser, dates


def quicken(qif_file, dates, organiser, account):
    """
    :type qif_file: file
    :type dates: list
    :param qif_file:
    :param dates:
    :param organiser:
    :param account:
    :return:
    """
    global keylist
    global numDict
    global specials_list

    qifs = make_qifs(qif_file)

    types = list(numDict.keys())

    for qif in qifs:
        if not qif.order['date'] in dates:
            dates.append(qif.order["date"])
        if not qif.order["date"] in organiser:
            organiser[qif.order["date"]] = []

        is_special = False
        for special_type in specials_list:
            if special_type.upper() in qif.order["payee"].upper():
                is_special = True
                break

        if (not qif.order["payee"] in keylist) and (not is_special):

            specialness = input(qif.order["payee"] + " for " + qif.order["amount"] + " on " + qif.textdate +
                                " is not a recognised transaction. Is this a generic transaction" +
                                "or part of a group of transactions? ")

            if specialness:
                keylist, specials_list = special_maker(qif.order["payee"], keylist, specials_list)

            else:
                # Then what kind of transaction is it?

                ktypeo = input("What type of transaction is " + qif.order["payee"] + " for " + qif.order[
                    "amount"] + " on " + qif.textdate + "? Bills, Food, Income, Gifts, Travel, Savings or Other: ")
                # ask for the type

                # make sure it is a valid type
                if not ktypeo in types:
                    vals = False
                    while not vals:
                        ktypeo = input(
                            "That is not a valid type of transaction, please enter either{0}.".format(str(types)) +
                            "Capitalisation is important: ")
                        # keep asking until it is a valid type
                        # Then it is a valid type
                        if ktypeo in types:
                            vals = True

                # We now know what type of transaction it is.
                for key in numDict.keys():
                    # so loop through the transaction types until we find the right one.
                    if ktypeo == key:
                        #increment the number of transactions we have of this type.
                        numDict[key] += 1
                        #and add it to the keylist.
                        keylist[qif.order["payee"]] = [ktypeo, numDict[key] - 1]

        organiser[qif.order["date"]].append(
            Transaction(qif.order["amount"], qif.order["payee"], account.name, qif.order["date"]))

    key_maker(keylist, specials_list)  # update keylist

    return organiser, dates


def hsbc(statement_file, dates, organiser, account):
    """
    A function to read out HSBC CSVs into the standardised format.
    (file, lst, dict) ---> dict, lst
    """

    global keylist
    global numDict
    global specials_list

    types = list(numDict.keys())
    with open(statement_file, 'r') as statement:
        reader = csv.reader(statement)

        for row in reader:
            dater = date_sorter(row[0])
            if not dater in dates:  # add to date list
                dates.append(dater)
            if not dater in organiser:  # add to object storage
                organiser[dater] = []

            # Check for specials
            is_special = False

            for special_type in specials_list:
                if special_type.upper() in row[1].upper():
                    is_special = True
                    break

            # start the process of adding an unknown to the keylist
            # If we can't find the key or it's not a special case
            if (not row[1] in keylist) and (not is_special):

                specialness = input(row[1] + " for " + row[2] + " on " + row[0] +
                                    " is not a recognised transaction. " +
                                    "Is this a generic transaction or part of a group of transactions? ")

                if specialness:
                    keylist, specials_list = special_maker(row[1], keylist, specials_list)

                else:
                    # Then what kind of transaction is it?
                    # ask for the type
                    ktypeo = input("What type of transaction is " + row[1] + " for " + row[2] + " on " + row[
                        0] + "? Bills, Food, Income, Gifts, Travel, Savings or Other: ")

                    #make sure it is a valid type
                    if not ktypeo in types:
                        vals = False
                        while not vals:
                            #keep asking until it is a valid type
                            ktypeo = input(
                                "That is not a valid type of transaction, please enter either{0}.".format(str(types)) +
                                "Capitalisation is important: ")
                            #Then it is a valid type
                            if ktypeo in types:
                                vals = True

                    #We now know what type of transaction it is.
                    for key in numDict.keys():
                        #so loop through the transaction types until we find the right one.
                        if ktypeo == key:
                            #increment the number of transactions we have of this type.
                            numDict[key] += 1
                            #and add it to the keylist.
                            keylist[row[1]] = [ktypeo, numDict[key] - 1]

            organiser[dater].append(Transaction(row[2], row[1], account.name, dater))

    # update keylist
    key_maker(keylist, specials_list)

    return organiser, dates


def halifax(statement_file, dates, organiser, account):
    """
    A function to read out Halifax CSVs into the standardised format.
    (file, lst, dict) ---> dict, lst
    """

    global keylist
    global numDict
    global specials_list

    types = list(numDict.keys())

    with open(statement_file, 'r') as statement:
        reader = csv.reader(statement)
        reader.__next__()

        for row in reader:
            try:
                row5 = Decimal(row[5])
            except:
                row5 = 0
            try:
                row6 = Decimal(row[6])
            except:
                row6 = 0

            datecomp = row[0][6:] + "-" + row[0][3:5] + "-" + row[0][:2]

            dater = date_sorter(row[0], 1)

            if not dater in dates:  # add to date list
                dates.append(dater)
            if not dater in organiser:  # add to object storage
                organiser[dater] = []

            if "CD 5333" in row[4]:
                typer1 = row[4].replace(" CD 5333", "")
                typer = typer1.rstrip()
            else:
                typer = row[4].rstrip()

            is_special = False

            for special_type in specials_list:
                if special_type.upper() in typer.upper():
                    is_special = True
                    break

                    # check if it is in the keylist or if it is a special case
            if (not typer in keylist) and (not is_special):

                specialness = input(typer + " for " + str(row6 - row5) + " on " + datecomp +
                                    " is not a recognised transaction." +
                                    " Is this a generic transaction or part of a group of transactions? ")

                # If it is special (above input to be turned into a bool using a checkbox.
                if specialness:
                    # what phraseare we using to test for specialness?
                    keylist, specials_list = special_maker(typer, keylist, specials_list)

                else:

                    # ask for the type
                    ktypeo = input("What type of transaction is " + typer + " for " + str(
                        row6 - row5) + " on " + datecomp + "? Bills, Food, Income, Gifts, Travel, Savings or Other: ")
                    # make sure it is a valid type
                    if not ktypeo in types:
                        vals = False
                        while not vals:
                            # keep asking until it is a valid type
                            ktypeo = input(
                                "That is not a valid type of transaction, please enter either{0}.".format(str(types)) +
                                "Capitalisation is important: ")
                            if ktypeo in types:
                                vals = True

                    # We now know what type of transaction it is.
                    for key in numDict.keys():
                        #so loop through the transaction types until we find the right one.
                        if ktypeo == key:
                            #increment the number of transactions we have of this type.
                            numDict[key] += 1
                            #and add it to the keylist.
                            keylist[typer] = [ktypeo, numDict[key] - 1]

            organiser[dater].append(Transaction(row6 - row5, typer, account.name, dater))

    # update keylist
    key_maker(keylist, specials_list)

    return organiser, dates

'''
////////////////////////////////////////////Start DB collating and gathering functions\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
'''

def date_splitter():
    """
    This function needs to take the main statement file and split it out into manageable and separable chunks.
    """
    dates = []  # set this to store the dates in order
    organiser = {}  # set this to organise all of the information but in manageable slices

    numm = 0
    numms = True

    while numms:
        try:
            numm = int(input("How many statements do you want to compile on this cycle? "))
            break
        except ValueError:
            print("That wasn't a number, please try again")

    for something in range(0, numm):

        banker = True
        typeo = input("Which account did this statement come from? " + str(account_list) + " ")

        # Don't know this bank
        if not typeo in account_list:
            banker = False

        # We need a known bank
        while not banker:
            typeo = input(
                "Sorry that account couldn't be found, you can either create another" +
                " account or choose from the list of already created accounts: " + str(
                    account_list) + " ")
            if typeo.upper() in ["HSBC", "HALIFAX"]:
                banker = True
            elif typeo.upper() == "CREATE ACCOUNT":
                typeo = create_account()
                break
        with open("core/accounts/" + typeo + ".pkl", "rb") as account_open:
            account = pickle.load(account_open)

            typeo = account.bank
            statement_file = input("Type in the filepath for statement " + str(something + 1) + " here: ")

            if not os.path.isfile(statement_file):
                is_real = False
                while not is_real:
                    statement_file = input(
                        "That file doesn't seem to exist, please enter the correct filepath for statement " + str(
                            something + 1) + " here: ")
                    if os.path.isfile(statement_file):
                        is_real = True

            # It's a Quicken file
            if statement_file.upper().endswith(".QIF"):
                organiser, dates = quicken(statement_file, dates, organiser, account)

            # It's a money file
            elif statement_file.upper().endswith(".OFX"):
                organiser, dates = OFX(statement_file, dates, organiser, account)

            # CSV from HSBC
            elif typeo.lower() == "hsbc":
                organiser, dates = hsbc(statement_file, dates, organiser, account)
                # So convert HSBC to standard format

            # CSV from Halifax
            elif typeo.lower() == "halifax":
                organiser, dates = halifax(statement_file, dates, organiser, account)
                # So convert Halifax to standard format.

    # get the dates in order
    dates.sort(reverse=True)

    dates = date_cleaner(dates)
    dates = list(set(dates))
    dates.sort()
    return organiser, dates


def dupli_clean(organiser, dates):
    """
    This function needs to take the now compiled list of transactions, which has been wiped of duplicates.
    It then needs to pickle each date for future reference (so as to not to steadily accumulate duplicates).
    Do I need a key system? probably not

    (dict, lst) ---> file
    """

    for date in dates:
        if not date in organiser:
            organiser[date] = []

        paths = "ref/" + str(date.year) + "/" + str(date.month) + "/"

        if not os.path.exists(paths):
            os.makedirs(paths)

        try:  # try open pickled object
            with open(paths + str(date.day) + ".pkl", "rb") as to_load:
                temp_date = pickle.load(to_load)
                # add all the transactions from the pickled object to the current transaction list
                organiser[date] = store[date] + temp_date.transactions

        except:
            pass

        date_obj = FullDate(organiser[date], date)  # create a new date object with the cleaned out file.
        with open(paths + str(date.day) + ".pkl", "wb") as new_date:
            pickle.dump(date_obj, new_date, pickle.HIGHEST_PROTOCOL)  # and pickle it for later reference

    return organiser


def sum_items(organiser):
    """
    Takes an organised dictionary of all the transactions for a day per type and sums them
    to create a total transaction amount for that type on that day.
    Now defunct due to replacement of organising system with objects.
    """
    for key in organiser:
        for innerKey in organiser[key]:
            organiser[key][innerKey] = sum(
                organiser[key][innerKey])  # summing all items and formatting to avoid Decimal point form issue
    return organiser


def object_sorter(store_object):
    obj_keys = list(store_object.keys())
    obj_keys.sort()

    for key_date in obj_keys:
        date_object = FullDate(store_object[key_date], key_date)
        store_object[key_date] = date_object

    return store_object


def type_splitter(datee, org, dictnum):
    """
    This function takes the list of dates, an organised dictionary of full_date objects
    containing the details of all transactions.

    Using this it creates a master dictionary containing sub dictionaries for each type.
    These sub-dictionaries in turn hold a set of sub-sub-dictionaries for each date,
    which hold the total transaction amount for that day for that type.
    """

    output_store = object_sorter(org)

    master_list = {}

    for key in dictnum.keys():
        master_list[key] = {}

    for date in datee:  # create a dictionary for each date
        day = str(date.day)
        month = str(date.month)
        year = str(date.year)

        if len(month) == 1:
            month = "0" + month

        if len(day) == 1:
            day = "0" + day

        act_date = year + "-" + month + "-" + day

        for key in master_list.keys():
            master_list[key][date] = [act_date]

            for q in range(0, dictnum[key]):
                master_list[key][date].append(0)

    # master_list = {"Type": dict for type,}

    # for each date
    for date1 in datee:
        if date1 in output_store:
            # find the key values within that date and loop through them
            for key in output_store[date1].name_totals.keys():
                # make sure it exists (no reason it wouldn't)
                if not key in keylist:
                    print(str(key) + " not found in keylist. Error occured")
                else:
                    master_list[keylist[key][0]][date1][keylist[key][1] + 1] = output_store[date1].name_totals[key]

    return master_list


def writer(master_list, datee, dict_num):
    """
    Takes an organised list of the sum of transactions on each day for each type,
     a list of dates represented, and the number of transactions for each type.

    Using this it prepopulates a CSV file with 0's after filling in a header for transaction types.
    It then systematically runs through the list of dates in order and fills each row of the csv with the data.
    """
    datee.sort()

    localfiles = []

    lists = {}

    for key in master_list.keys():
        lists[key] = []
        for q in range(0, dict_num[key]):
            lists[key].append(0)
    for ii in keylist:  # run through the transactions
        lists[keylist[ii][0]][keylist[ii][1]] = ii

    for csv_file in os.listdir("core/csvs"):
        if csv_file.endswith(".csv"):
            localfiles.append("core/csvs/" + csv_file)

    for csv_file in localfiles:
        key = csv_file.replace(".csv", "")
        key = key.replace("core/csvs/", "")

        with open(csv_file, "w") as writing:
            csv_writer = csv.writer(writing)
            csv_writer.writerow([""] + lists[key])

            for date in datee:
                while len(master_list[key][date]) < len(lists[key]):
                    master_list[key][date].append(0)
                csv_writer.writerow(master_list[key][date])
