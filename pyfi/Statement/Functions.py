"""
The module to set up the major functions concerning normalising transactions and storing them in a presentable and
accessible way.

TODO: Create a user-defined way of reading a csv.
"""

#////////////////////////////////////////////Start format Standardisation Functions\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
def OFX(filename, dates, organiser, account):
    global keylist
    global specials_list
    global numDict

    transactions = []

    types = list(numDict.keys())

    unknowns = {}
    unknownstodo = []

    with open(filename, 'r') as old:

        intrans = False

        for line in old:
            line = line.lstrip()
            if intrans:
                if line.startswith('</STMTTRN>'):
                    intrans = False
                    use = None
                    for combo in [trans_name + trans_memo, trans_name + ' ' + trans_memo, trans_name, trans_memo]:
                        if '&amp;' in combo:
                            combo = combo.replace('&amp;', '&')
                        if combo in keylist:
                            #print('found', combo)
                            use = combo
                            break
                        elif combo in specials_list:
                            use = combo
                            break
                    else:
                        if not [trans_name + ' ' + trans_memo] in unknowns.keys():
                            unknowns[trans_name + ' ' + trans_memo] = [newtrans["amount"], newtrans["date"]]
                        else:
                            unknownstodo.append([trans_name + ' ' + trans_memo, newtrans["amount"], newtrans["date"]])

                    if not use is None :
                        newtrans['name'] = use
                        transactions.append(Classes.Transaction(newtrans['amount'], newtrans['name'], newtrans['account_name'],
                                                    Classes.date_sorter(newtrans['date'])))

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

    if len(unknowns.keys())>0:
        transactions = transactions + get_unknowns(unknowns = unknowns, numbered_dictionary = numDict, account = account)
    if len(unknownstodo)>0:
        for trans in unknownstodo:
            transactions.append(Classes.Transaction(trans[1], trans[0], account, Classes.datetime.date(int(trans[2][:4]),
                                                                                       int(trans[2][5:7]),
                                                                                       int(trans[2][8:10]))))
    if transactions is None:
        return None, None
    else:

        for trans in transactions:
            if trans.date not in dates:
                dates.append(trans.date)
            if trans.date not in organiser:
                organiser[trans.date] = []
            organiser[trans.date].append(trans)


        Classes.key_maker(keylist, specials_list)

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

    qifs = Classes.make_qifs(qif_file)

    types = list(numDict.keys())
    transactions = []
    unknowns = {}
    unknownstodo = []

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
            if not qif.order["payee"] in unknowns.keys():
                unknowns[qif.order["payee"]]=[qif.order["amount"], qif.textdate]
            else:
                unknownstodo.append([qif.order["payee"], qif.order["amount"], qif.textdate])


        else:
            transactions.append(Classes.Transaction(qif.order["amount"], qif.order["payee"], account, qif.order["date"]))


    if len(unknowns.keys())>0:
        transactions = transactions + get_unknowns(unknowns = unknowns,
                                                   numbered_dictionary = numDict,
                                                   account = account)
    if len(unknownstodo)>0:
        for trans in unknownstodo:
            transactions.append(Classes.Transaction(trans[1], trans[0], account, Classes.datetime.date(int(trans[2][:4]),
                                                                                       int(trans[2][5:7]),
                                                                                       int(trans[2][8:10]))))
    if transactions is None:
        return None, None
    else:

        for trans in transactions:
            if trans.date not in dates:
                dates.append(trans.date)
            if trans.date not in organiser:
                organiser[trans.date] = []
            organiser[trans.date].append(trans)

        Classes.key_maker(keylist, specials_list)  # update keylist

        return organiser, dates