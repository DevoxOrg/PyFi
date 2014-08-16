from main import *
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from pylab import *

#experimental at the moment - graph creation.

def graph_maker(everything=1, date1="Beginning", date2="End"):

    if everything:
        all_trans = get_all(everything)
    else:
        all_trans = get_all(date1, date2)

    dates = list(all_trans.keys())
    dates.sort()
    transactions = []
    for date in dates:
        num = 0
        for trans in all_trans[date].transactions:
            num += trans.amount
        transactions.append(num)
        
    plt.plot_date(dates, transactions, linestyle='-', fmt="bo", lod=False)
    plt.show()
    #return dates, transactions


def pie_maker(everything, compare=None, date1="Beginning", date2="End",
              trans_types=list(numDict.keys()), accounts=account_list):

    if compare is None:
        if everything:
            all_trans = get_all(everything)
        else:
            all_trans = get_all(everything, date1, date2, trans_types, accounts)

        trans_types = {}
        for date in all_trans:
            for typ in all_trans[date].type_totals:
                if typ not in trans_types:
                    trans_types[typ] = 0
                trans_types[typ] += all_trans[date].type_totals[typ]

    amounts = []
    labels = []
    explode = []
    greatest = 0
    for typ in trans_types:
        if trans_types[typ] < 0:
            labels.append(typ + " ("+str(abs(trans_types[typ]))+")")
            amounts.append(abs(trans_types[typ]))
            if abs(trans_types[typ]) > greatest:
                greatest = abs(trans_types[typ])
    for i in range(len(amounts)):
        explode.append(0)
    explode[amounts.index(greatest)] = 0.05

    figure(1, figsize=(12, 10))

    plt.pie(amounts, labels=labels, explode=explode, shadow=True, startangle=90, autopct='%1.1f%%')

    plt.show()
