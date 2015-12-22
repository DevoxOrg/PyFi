"""
The running program. start() starts everything and it should be from here where things are run.

Defines a few overarching functions.
"""

import Statement.Classes as sc
import Statement.Functions as sf
import sys, datetime, pickle
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

