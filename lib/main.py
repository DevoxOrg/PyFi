"""
The running program. start() starts everything and it should be from here where things are run.

Defines a few overarching functions.

TODO: sort out configs so they're independent of this file.
"""

import Statement.Classes as sc
import Statement.Functions as sf
import sys
from UI import ui

def start(write=False, account = None, statement_file = None):
    """
    Function holds the bulk of the statement compiler and csv building mechanism

    An optional parameter decides if we rewrite the CSV's after updating the reference files.

    (bool) ---> CSV/Reference files
    """

    # compile the csvs, generate the transaction dictionary and a list of dates.
    transactions, date_list = sf.date_splitter(statement_file, account)

    if transactions is None:
        return None
    else:
        # Check against previous records or that date.
        # Clean out duplicates, update the transaction dictionary and update the records of that date.
        sf.dupli_clean(transactions, date_list)

    if write:  # are we making CSV's?
        csv_writer(True)


def csv_writer(everything = True, date1="Beginning", date2="End", types=list(sc.numDict.keys()), accounts=sc.account_list):
    """
    A custom CSV writer to create CSV's with all the transactions between a set of dates.

    Default values ensure that all dates with a fully implemented reference system are used.

    First parameter is a bool that if True forces the whole reference directory to be sued.
    If False we refer to date1 and date2, date1 being the initial date and date2 being the final date (inclusive)
    as our frame of reference to include in the CSVs.

    (bool, str, str) ---> csv*
    """
    global numDict

    transactions = sc.get_all(everything, date1, date2, types, accounts)

    dates = list(transactions.keys())
    dates.sort(reverse=True)
    dates = sc.date_cleaner(dates)

    for date in dates:
        if date in transactions.keys():
            transactions[date] = transactions[date].transactions
        else:
            transactions[date] = []

    master = sf.type_splitter(dates, transactions, numDict)

    sf.writer(master, dates, numDict)


#///////////////////////////////////////////// Start Controller classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class ControlMainWidget(ui.QtGui.QWidget):
    def __init__(self, numbered_dictionary, accounts, parent=None, Widg = ui.Opener()):
        super(ControlMainWidget, self).__init__(parent)
        self.widget = Widg
        self.widget.setupUi(self)
        #print(Widg)
        if isinstance(Widg, ui.Opener):
            #print(1)
            ui.QtCore.QObject.connect(self.widget.toolButton, ui.QtCore.SIGNAL('clicked()'),
                                   lambda:MainWidgetChange(parent, widg=ui.StatsView()))

            ui.QtCore.QObject.connect(self.widget.toolButton_2, ui.QtCore.SIGNAL('clicked()'),
                                   lambda:MainWidgetChange(parent, widg=ui.GraphicalView()))

            ui.QtCore.QObject.connect(self.widget.toolButton_3, ui.QtCore.SIGNAL('clicked()'),
                                   lambda:MainWidgetChange(parent, widg=ui.StatementView(accounts)))

            ui.QtCore.QObject.connect(self.widget.toolButton_4, ui.QtCore.SIGNAL('clicked()'),
                                   lambda:MainWidgetChange(parent, widg=ui.TableView()))
       # print(2)


class ControlMainWindow(ui.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = ui.Ui_MainWindow(csv_writer, sc.account_list)
        self.ui.setupUi(self)

        # bit of an awkward hack putting these here...

        self.ui.actionChangeHome.triggered.connect(lambda: MainWidgetChange(self, widg = ui.Opener()))
        self.ui.actionChangeStat.triggered.connect(lambda: MainWidgetChange(self, widg = ui.StatsView()))
        self.ui.actionChangeState.triggered.connect(lambda: MainWidgetChange(self, widg = ui.StatementView(sc.account_list)))
        self.ui.actionChangeTab.triggered.connect(lambda: MainWidgetChange(self, widg = ui.TableView()))
        self.ui.actionChangeGraph.triggered.connect(lambda: MainWidgetChange(self, widg = ui.GraphicalView()))

#///////////////////////////////////////////// End Controller classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

def MainWidgetChange(Window, widg = ui.Opener()):

    the_widget = ControlMainWidget(sc.numDict, sc.account_list, parent = Window, Widg = widg)

    Window.setCentralWidget(the_widget)

if __name__ == '__main__':
    app = ui.QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    MainWidgetChange(mySW)
    mySW.show()
    sys.exit(app.exec_())

