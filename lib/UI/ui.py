# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Sep 15 13:11:21 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!


"""
This may be in competition with mainui2.py for the main ui module, I think this one is winning.

Set up the major ui widgets and their functions - large file, consider splitting
"""


from csv import reader
from decimal import Decimal
from os import listdir

from PySide import QtCore, QtGui

import numpy as np
import matplotlib

matplotlib.use('QT4Agg')
matplotlib.rcParams['backend.qt4'] = 'PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import  Figure
import matplotlib.pyplot as plt

import pickle, datetime, sys

sys.path.append('../')

from Statement.Classes import get_all, Account, TypeObject, keylist_cleaner, list_grabber
#/////////////////////////////////////////////// Start Popup/Dialog classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

redfont = QtGui.QBrush()
redfont.setColor("red")

class Statement_Popup(object):
    def __init__(self, accounts):
        self.accounts = accounts
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 156)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        
        self.comboBox.addItem("")
        
        for account in enumerate(self.accounts):
            self.comboBox.addItem("")
            self.comboBox.setItemText(account[0]+1, account[1])

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.retranslateUi(Dialog)

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.showDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), lambda: self.validate(Dialog))
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def validate(self, Dialog):
        Errored = False
        if self.comboBox.currentText() == "Please Select...":
            Errored = True
            if self.gridLayout.itemAtPosition(1, 2) != 0:
                self.gridLayout.addWidget(QtGui.QLabel("Missing Answer", Dialog), 1, 2, 1, 1)

        if self.lineEdit.text() == "Enter filepath here...":
            Errored = True
            if self.gridLayout.itemAtPosition(0, 3) != 0:
                self.gridLayout.addWidget(QtGui.QLabel("Missing Answer", Dialog), 0, 3, 1, 1)

        if not Errored:
            Dialog.accept()

    def get_values(self):
        return self.comboBox.currentText(), self.lineEdit.text()

    def showDialog(self):

        fname, waste = QtGui.QFileDialog.getOpenFileName(caption = "Browse...")

        self.lineEdit.setText(fname)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "Enter filepath here...", None,
                                                           QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Please Select...", None,
                                                                  QtGui.QApplication.UnicodeUTF8))

class Account_Popup(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(302, 107)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 3, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 2, 1, 2)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 2)
        self.error = None
        self.error2 = None

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), lambda: self.acceptance(Dialog))
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def acceptance(self, Dialog):
        typ = self.lineEdit.text()

        errored = False

        if typ + ".pkl" in listdir("../core/accounts"):
            if not self.error == QtGui.QLabel("This account already exists, enter a new account.", Dialog):
                if self.gridLayout.itemAtPosition(0, 4):
                    self.error.setText("This account already exists, enter a new account.")
                else:
                    self.error = QtGui.QLabel("This account already exists, enter a new account.", Dialog)
                    self.gridLayout.addWidget(self.error, 0,4,1,1)

            errored = True
        elif typ == "Please enter the account name here...":
            if not self.error == QtGui.QLabel("Missing answer", Dialog):
                if self.gridLayout.itemAtPosition(0, 4):
                    self.error.setText("Missing answer")
                else:
                    self.error = QtGui.QLabel("Missing answer", Dialog)
                    self.gridLayout.addWidget(self.error, 0,4,1,1)
            errored = True

        if self.comboBox.currentText() == "Which bank holds this account?":
            if not self.error2 == QtGui.QLabel("Missing answer", Dialog):
                if self.gridLayout.itemAtPosition(1, 4):
                    self.error2.setText("Missing answer")
                else:
                    self.error2 = QtGui.QLabel("Missing answer", Dialog)
                    self.gridLayout.addWidget(self.error2, 1,4,1,1)
            errored = True

        if not errored:
            typical = Account(name = typ, bank = self.comboBox.currentText(), savings = self.checkBox.isChecked())
            with open("../core/accounts/" + typ + ".pkl", "wb") as new_type:
                pickle.dump(typical, new_type, protocol=pickle.HIGHEST_PROTOCOL)
            Dialog.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Bank Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Account Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Is Savings", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "Which bank holds this account?", None,
                                                                  QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "HSBC", None,
                                                                  QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "Halifax", None,
                                                                  QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "Please enter the account name here...", None,
                                                           QtGui.QApplication.UnicodeUTF8))

class Type_Popup(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(308, 101)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.error = None
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), lambda: self.acceptance(Dialog))
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def acceptance(self, Dialog):
        typ = self.lineEdit.text()


        if typ + ".pkl" in listdir("../core/types"):
            if not self.error == QtGui.QLabel("This type already exists, enter a new type.", Dialog):
                if self.gridLayout.itemAtPosition(0, 2):
                    self.error.setText("This type already exists, enter a new type.")
                else:
                    self.error = QtGui.QLabel("This type already exists, enter a new type.", Dialog)
                    self.gridLayout.addWidget(self.error, 0,2,1,1)
        elif typ == "Please enter the name of this type here...":
            if not self.error == QtGui.QLabel("Missing answer", Dialog):
                if self.gridLayout.itemAtPosition(0, 2):
                    self.error.setText("Missing answer")
                else:
                    self.error = QtGui.QLabel("Missing answer", Dialog)
                    self.gridLayout.addWidget(self.error, 0,2,1,1)
        else:
            typical = TypeObject(typ = typ)
            with open("../core/types/" + typ + ".pkl", "wb") as new_type:
                pickle.dump(typical, new_type, protocol=pickle.HIGHEST_PROTOCOL)
            #numDict[typ] = 0
            Dialog.accept()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("Dialog", "Please enter the name of this type here...", None,
                                                           QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Type Name ", None, QtGui.QApplication.UnicodeUTF8))

class TransAdder(object):
    def __init__(self, unknowns, numbered_dictionary):
        self.unknowns = unknowns
        self.types = ["Please Select..."]

        for trans_typ in numbered_dictionary:
            self.types.append(trans_typ)

        self.unknown_keys = sorted(list(unknowns.keys()))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setMinimumSize(600, 300)
        Dialog.setMaximumSize(1200, 800)
        #Dialog.resize(431, 93)
        self.maingrid = QtGui.QGridLayout(Dialog)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.verticalLayout = QtGui.QGridLayout(self.groupBox)
        self.label = QtGui.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setMaximumHeight(40)
        self.verticalLayout.addWidget(self.label, 0, 0, 2, 2)
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(False)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.unknown_trans = {}
        self.row = 1



        for key in self.unknown_keys:
            self.unknown_trans[key] = [QtGui.QLabel(self.scrollAreaWidgetContents),
                                       QtGui.QComboBox(self.scrollAreaWidgetContents),
                                       QtGui.QPushButton(self.scrollAreaWidgetContents)]
            self.unknown_trans[key][0].setText("Transaction " + key + " for " + self.unknowns[key][0] + " on " +
                                          self.unknowns[key][1]+":")
            self.unknown_trans[key][2].setText("Add Group")
            self.unknown_trans[key][1].addItems(self.types)

            self.unknown_trans[key][0].setObjectName("Label" + str(self.row))
            self.unknown_trans[key][1].setObjectName("Combo" + str(self.row))
            self.unknown_trans[key][2].setObjectName("Button" + str(self.row))

            self.gridLayout.addWidget(self.unknown_trans[key][0], self.row, 0, 1, 1)
            self.gridLayout.addWidget(self.unknown_trans[key][1], self.row, 1, 1, 1)
            self.gridLayout.addWidget(self.unknown_trans[key][2], self.row, 2, 1, 1)
            self.row += 1

        '''self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)'''
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, self.row, 1, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea, 2, 0, 10, 10)
        self.maingrid.addWidget(self.label, 0, 0, 1, 2)
        self.maingrid.addWidget(self.groupBox, 1, 0, 1, 2)
        self.maingrid.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), lambda: self.validate(Dialog))
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def validate(self, Dialog):
        counting = 1
        Errored = False
        for key in self.unknowns:
            if self.unknown_trans[key][1].currentText() == "Please Select...":
                if self.gridLayout.itemAtPosition(counting, 3) != 0:
                    self.gridLayout.addWidget(QtGui.QLabel("Missing Answer", Dialog), counting, 3, 1, 1)

                Errored = True
                self.sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

            counting += 1

        if not Errored:
            Dialog.accept()

    def get_values(self):
        for key in self.unknowns:
            self.unknowns[key] = self.unknown_trans[key][1].currentText()

        return self.unknowns

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        #self.label_2.setText(QtGui.QApplication.translate("Dialog",
         #                                                 "Transaction something for this amount on this date:", None,
          #                                                QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog",
                                                        "The following transactions have not been recognised. Please enter their types for future reference:", None,
                                                        QtGui.QApplication.UnicodeUTF8))
        #self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Add Group", None,
         #                                                    QtGui.QApplication.UnicodeUTF8))


class DialogWidg(QtGui.QDialog):
    def __init__(self, typer, accounts = None, unknowns = None, numbered_dictionary = None, parent=None):
        super(DialogWidg, self).__init__(parent)
        if typer == 'Statement':
            self.widg = Statement_Popup(accounts=accounts)
        elif typer == 'Account':
            self.widg = Account_Popup()
        elif typer == 'Type':
            self.widg = Type_Popup()
        elif typer == "TransAdder":
            self.widg = TransAdder(unknowns, numbered_dictionary)

        self.widg.setupUi(self)


#/////////////////////////////////////////////// End Popup/Dialog classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#///////////////////////////////////////////// Start Central Widget classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class StatementView(object):
    def __init__(self, accounts, numbered_dictionary, some_func):
        self.accounts = accounts
        self.numbered_dictionary = numbered_dictionary
        self.some_func = some_func
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(563, 524)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(Form)
        self.groupBox_5.setMaximumSize(QtCore.QSize(16777215, 90))
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.scrollArea_2 = QtGui.QScrollArea(self.groupBox_5)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 73, 84))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.account_checks = []

        for account in enumerate(self.accounts):
            self.account_checks.append(QtGui.QCheckBox(self.scrollAreaWidgetContents_2))
            self.account_checks[account[0]].setObjectName(account[1]+'_filter')
            self.account_checks[account[0]].setText(account[1])
            self.verticalLayout_3.addWidget(self.account_checks[account[0]])

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.addWidget(self.scrollArea_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_5, 0, 1, 3, 1)
        self.groupBox_4 = QtGui.QGroupBox(Form)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 90))
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea = QtGui.QScrollArea(self.groupBox_4)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 77, 84))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.typ_checks = []

        for trans_typ in enumerate(self.numbered_dictionary):
            self.typ_checks.append(QtGui.QCheckBox(self.scrollAreaWidgetContents))
            self.typ_checks[trans_typ[0]].setObjectName(trans_typ[1]+'_filter')
            self.typ_checks[trans_typ[0]].setText(trans_typ[1])
            self.verticalLayout_2.addWidget(self.typ_checks[trans_typ[0]])


        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_4, 0, 2, 3, 1)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dateEdit = QtGui.QDateEdit(self.groupBox)
        self.dateEdit.setMaximumDate(QtCore.QDate(2030, 12, 31))
        self.dateEdit.setMinimumDate(QtCore.QDate(1990, 1, 1))
        self.dateEdit.setDateTime(QtCore.QDateTime(2000,1,1,1,1,1,1,0))
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout_2.addWidget(self.dateEdit, 1, 0, 1, 1)
        self.dateEdit_2 = QtGui.QDateEdit(self.groupBox)
        self.dateEdit_2.setMaximumDate(QtCore.QDate(2030, 12, 31))
        self.dateEdit_2.setMinimumDate(QtCore.QDate(1990, 1, 1))
        self.dateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout_2.addWidget(self.dateEdit_2, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 3, 3, 1)
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 0, 1, 1)
        self.tableWidget = QtGui.QTableWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())

        all_things = self.some_func(True)

        all_keys = list(all_things.keys())

        all_keys.sort()

        all_list = []

        for key in all_keys:
            for innerKey in all_things[key].transactions:
                date_add = str(key.year)+'/'
                if len(str(key.month)) == 1:
                    date_add = date_add + '0' + str(key.month)+'/'
                else:
                    date_add = date_add+str(key.month)+'/'
                if len(str(key.day)) == 1:
                    date_add = date_add + '0' + str(key.day)
                else:
                    date_add = date_add+str(key.day)

                all_list.append([date_add,
                                 innerKey.account,
                                 innerKey.type,
                                 innerKey.name,
                                 innerKey.amount])


        self.colcnt = 5

        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)

        if len(all_list)>0:
            self.rowcnt = len(all_list)
            #print(1)
        else:
            #print(2)
            self.rowcnt = self.popup_statement()
            all_things = self.some_func(True)

            all_keys = list(all_things.keys())

            all_keys.sort()

            all_list = []

            for key in all_keys:
                for innerKey in all_things[key].transactions:
                    date_add = str(key.year)+'/'
                    if len(str(key.month)) == 1:
                        date_add = date_add + '0' + str(key.month)+'/'
                    else:
                        date_add = date_add+str(key.month)+'/'
                    if len(str(key.day)) == 1:
                        date_add = date_add + '0' + str(key.day)
                    else:
                        date_add = date_add+str(key.day)

                    all_list.append([date_add,
                                     innerKey.account,
                                     innerKey.type,
                                     innerKey.name,
                                     innerKey.amount])


            self.colcnt = 5

            self.tableWidget.setSizePolicy(sizePolicy)
            self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(5)


        self.tableWidget.setRowCount(self.rowcnt)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        if len(all_list)>0:
            for row in range(self.rowcnt):
                for col in range(self.colcnt):
                    if '-' in str(all_list[row][col]) and col == self.colcnt-1:
                        item = QtGui.QTableWidgetItem(str(all_list[row][col]))

                        item.setForeground(redfont)
                    else:
                        item = QtGui.QTableWidgetItem(str(all_list[row][col]))
                    #item = QtGui.QTableWidgetItem(str(all_list[row][col]))
                    self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.gridLayout.addWidget(self.tableWidget, 3, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL('clicked()'), self.fill_table)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.popup_statement)

    def popup_statement(self):
        from main import start
        self.pops = DialogWidg('Statement', accounts=self.accounts)
        if self.pops.exec_():
            account, filepath = self.pops.widg.get_values()
            start(statement_file = filepath, account = account)

            return self.fill_table()

    def fill_table(self):

        beginning, end, types, accounts = self.find_filters()

        all_things = self.some_func(False, beginning, end, types, accounts)

        #print(beginning,end,types,accounts)

        all_keys = list(all_things.keys())

        all_keys.sort()

        all_list = []

        for key in all_keys:
            #print(all_things[key])
            for innerKey in all_things[key].transactions:
                #print(innerKey)
                dateuse = str(key.year)+"/"
                if len(str(key.month)) == 1:
                    dateuse += '0'+str(key.month)+'/'
                else:
                    dateuse += str(key.month)+'/'
                if len(str(key.day)) == 1:
                    dateuse += '0'+str(key.day)
                else:
                    dateuse += str(key.day)


                all_list.append([dateuse, innerKey.account, innerKey.type,
                                  innerKey.name, innerKey.amount])

        self.rowcnt = len(all_list)
        #print(self.rowcnt, len(all_keys), len(all_things))
        if self.rowcnt == 0:
            self.tableWidget.setRowCount(self.rowcnt)
        else:
            colcnt = len(all_list[0])
            self.tableWidget.setRowCount(self.rowcnt)
            for row in range(self.rowcnt):
                for col in range(colcnt):
                    if '-' in str(all_list[row][col]) and col == self.colcnt-1:
                        item = QtGui.QTableWidgetItem(str(all_list[row][col]))

                        item.setForeground(redfont)
                    else:
                        item = QtGui.QTableWidgetItem(str(all_list[row][col]))
                    self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()

        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        return self.rowcnt

    def find_filters(self):
        types = []
        for widget in self.scrollAreaWidgetContents.children():
            if isinstance(widget, QtGui.QCheckBox):
                if widget.isChecked():
                    types.append(widget.text())

        if len(types) == 0:
            for widget in self.scrollAreaWidgetContents.children():
                if isinstance(widget, QtGui.QCheckBox):
                    types.append(widget.text())

        accounts = []
        for widget in self.scrollAreaWidgetContents_2.children():
            if isinstance(widget, QtGui.QCheckBox):
                if widget.isChecked():
                    accounts.append(widget.text())

        if len(accounts) == 0:
            for widget in self.scrollAreaWidgetContents_2.children():
                if isinstance(widget, QtGui.QCheckBox):
                    accounts.append(widget.text())

        beginning = str(self.dateEdit.date().year())+'-'

        if len(str(self.dateEdit.date().month())) == 1:
            beginning = beginning +'0'+str(self.dateEdit.date().month())+'-'
        else:
            beginning = beginning +str(self.dateEdit.date().month())+'-'

        if len(str(self.dateEdit.date().month())) == 1:
            beginning = beginning +'0'+str(self.dateEdit.date().day())
        else:
            beginning = beginning +str(self.dateEdit.date().day())

        end = str(self.dateEdit_2.date().year())+'-'

        if len(str(self.dateEdit_2.date().month())) == 1:
            end = end +'0'+str(self.dateEdit_2.date().month())+'-'
        else:
            end = end +str(self.dateEdit_2.date().month())+'-'

        if len(str(self.dateEdit_2.date().month())) == 1:
            end = end +'0'+str(self.dateEdit_2.date().day())
        else:
            end = end +str(self.dateEdit_2.date().day())

        return beginning, end, types, accounts

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Import Statement", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("Form", "Account Filters", None,
                                                              QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Form", "Type Filters", None,
                                                              QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Date Filter", None,
                                                            QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Form", "Pi Chart!", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "Apply Filter", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "1", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "2", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "3", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(3).setText(QtGui.QApplication.translate("Form", "4", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(4).setText(QtGui.QApplication.translate("Form", "5", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(5).setText(QtGui.QApplication.translate("Form", "6", None,
                                                                                    QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "Date", None,
                                                                                      QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Account", None,
                                                                                      QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Type", None,
                                                                                      QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Form", "Transaction", None,
                                                                                      QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Form", "Amount", None,
                                                                                      QtGui.QApplication.UnicodeUTF8))


class Opener(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 400)
        Form.setMinimumSize(QtCore.QSize(450, 400))
        Form.setMaximumSize(QtCore.QSize(450, 400))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton = QtGui.QToolButton(Form)
        self.toolButton.setMinimumSize(QtCore.QSize(150, 150))
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 0, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(Form)
        self.toolButton_2.setMinimumSize(QtCore.QSize(150, 150))
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 0, 1, 1, 1)
        self.toolButton_3 = QtGui.QToolButton(Form)
        self.toolButton_3.setMinimumSize(QtCore.QSize(150, 150))
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 1, 0, 1, 1)
        self.toolButton_4 = QtGui.QToolButton(Form)
        self.toolButton_4.setMinimumSize(QtCore.QSize(150, 150))
        self.toolButton_4.setObjectName("toolButton_4")
        self.gridLayout.addWidget(self.toolButton_4, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("Form", "Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("Form", "Graphs", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_3.setText(QtGui.QApplication.translate("Form", "Statement", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.toolButton_4.setText(QtGui.QApplication.translate("Form", "Tables", None,
                                                               QtGui.QApplication.UnicodeUTF8))

class StatsView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(904, 769)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")

        #start headliners

        self.tot_spend = QtGui.QLabel(Form)
        self.tot_spend.setObjectName("tot_spend")
        self.gridLayout.addWidget(self.tot_spend, 0, 0, 1, 1)
        self.av_mon_net = QtGui.QLabel(Form)
        self.av_mon_net.setObjectName("av_mon_net")
        self.gridLayout.addWidget(self.av_mon_net, 2, 2, 1, 1)
        self.tot_in = QtGui.QLabel(Form)
        self.tot_in.setObjectName("tot_in")
        self.gridLayout.addWidget(self.tot_in, 1, 0, 1, 1)
        self.av_mon_net_num = QtGui.QLabel(Form)
        self.av_mon_net_num.setObjectName("av_mon_net_num")
        self.gridLayout.addWidget(self.av_mon_net_num, 2, 3, 1, 1)
        self.av_mon_spend_num = QtGui.QLabel(Form)
        self.av_mon_spend_num.setObjectName("av_mon_spend_num")
        self.gridLayout.addWidget(self.av_mon_spend_num, 0, 3, 1, 1)
        self.av_mon_in = QtGui.QLabel(Form)
        self.av_mon_in.setObjectName("av_mon_in")
        self.gridLayout.addWidget(self.av_mon_in, 1, 2, 1, 1)
        self.av_mon_spend = QtGui.QLabel(Form)
        self.av_mon_spend.setObjectName("av_mon_spend")
        self.gridLayout.addWidget(self.av_mon_spend, 0, 2, 1, 1)
        self.tot_spend_num = QtGui.QLabel(Form)
        self.tot_spend_num.setObjectName("tot_spend_num")
        self.gridLayout.addWidget(self.tot_spend_num, 0, 1, 1, 1)
        self.av_mon_in_num = QtGui.QLabel(Form)
        self.av_mon_in_num.setObjectName("av_mon_in_num")
        self.gridLayout.addWidget(self.av_mon_in_num, 1, 3, 1, 1)
        self.net_in_num = QtGui.QLabel(Form)
        self.net_in_num.setObjectName("net_in_num")
        self.gridLayout.addWidget(self.net_in_num, 2, 1, 1, 1)
        self.tot_in_num = QtGui.QLabel(Form)
        self.tot_in_num.setObjectName("tot_in_num")
        self.gridLayout.addWidget(self.tot_in_num, 1, 1, 1, 1)
        self.net_in = QtGui.QLabel(Form)
        self.net_in.setObjectName("net_in")
        self.gridLayout.addWidget(self.net_in, 2, 0, 1, 1)

        #start monthly income group
        self.av_mon_in_group = QtGui.QGroupBox(Form)
        self.av_mon_in_group.setObjectName("av_mon_in_group")
        self.gridLayout_8 = QtGui.QGridLayout(self.av_mon_in_group)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.in_jan = QtGui.QLabel(self.av_mon_in_group)
        self.in_jan.setObjectName("in_jan")
        self.gridLayout_8.addWidget(self.in_jan, 0, 0, 1, 1)
        self.in_feb = QtGui.QLabel(self.av_mon_in_group)
        self.in_feb.setObjectName("in_feb")
        self.gridLayout_8.addWidget(self.in_feb, 0, 1, 1, 1)
        self.in_mar = QtGui.QLabel(self.av_mon_in_group)
        self.in_mar.setObjectName("in_mar")
        self.gridLayout_8.addWidget(self.in_mar, 0, 2, 1, 1)
        self.in_apr = QtGui.QLabel(self.av_mon_in_group)
        self.in_apr.setObjectName("in_apr")
        self.gridLayout_8.addWidget(self.in_apr, 0, 3, 1, 1)
        self.in_may = QtGui.QLabel(self.av_mon_in_group)
        self.in_may.setObjectName("in_may")
        self.gridLayout_8.addWidget(self.in_may, 0, 4, 1, 1)
        self.in_jun = QtGui.QLabel(self.av_mon_in_group)
        self.in_jun.setObjectName("in_jun")
        self.gridLayout_8.addWidget(self.in_jun, 0, 5, 1, 1)
        self.in_jul = QtGui.QLabel(self.av_mon_in_group)
        self.in_jul.setObjectName("in_jul")
        self.gridLayout_8.addWidget(self.in_jul, 0, 6, 1, 1)
        self.in_aug = QtGui.QLabel(self.av_mon_in_group)
        self.in_aug.setObjectName("in_aug")
        self.gridLayout_8.addWidget(self.in_aug, 0, 7, 1, 1)
        self.in_sep = QtGui.QLabel(self.av_mon_in_group)
        self.in_sep.setObjectName("in_sep")
        self.gridLayout_8.addWidget(self.in_sep, 0, 8, 1, 1)
        self.in_oct = QtGui.QLabel(self.av_mon_in_group)
        self.in_oct.setObjectName("in_oct")
        self.gridLayout_8.addWidget(self.in_oct, 0, 9, 1, 1)
        self.in_nov = QtGui.QLabel(self.av_mon_in_group)
        self.in_nov.setObjectName("in_nov")
        self.gridLayout_8.addWidget(self.in_nov, 0, 10, 1, 1)
        self.in_dec = QtGui.QLabel(self.av_mon_in_group)
        self.in_dec.setObjectName("in_dec")
        self.gridLayout_8.addWidget(self.in_dec, 0, 11, 1, 1)
        self.in_jan_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_jan_num.setObjectName("in_jan_num")
        self.gridLayout_8.addWidget(self.in_jan_num, 1, 0, 1, 1)
        self.in_feb_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_feb_num.setObjectName("in_feb_num")
        self.gridLayout_8.addWidget(self.in_feb_num, 1, 1, 1, 1)
        self.in_mar_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_mar_num.setObjectName("in_mar_num")
        self.gridLayout_8.addWidget(self.in_mar_num, 1, 2, 1, 1)
        self.in_apr_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_apr_num.setObjectName("in_apr_num")
        self.gridLayout_8.addWidget(self.in_apr_num, 1, 3, 1, 1)
        self.in_may_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_may_num.setObjectName("in_may_num")
        self.gridLayout_8.addWidget(self.in_may_num, 1, 4, 1, 1)
        self.in_jun_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_jun_num.setObjectName("in_jun_num")
        self.gridLayout_8.addWidget(self.in_jun_num, 1, 5, 1, 1)
        self.in_jul_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_jul_num.setObjectName("in_jul_num")
        self.gridLayout_8.addWidget(self.in_jul_num, 1, 6, 1, 1)
        self.in_aug_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_aug_num.setObjectName("in_aug_num")
        self.gridLayout_8.addWidget(self.in_aug_num, 1, 7, 1, 1)
        self.in_sep_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_sep_num.setObjectName("in_sep_num")
        self.gridLayout_8.addWidget(self.in_sep_num, 1, 8, 1, 1)
        self.in_oct_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_oct_num.setObjectName("in_oct_num")
        self.gridLayout_8.addWidget(self.in_oct_num, 1, 9, 1, 1)
        self.in_nov_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_nov_num.setObjectName("in_nov_num")
        self.gridLayout_8.addWidget(self.in_nov_num, 1, 10, 1, 1)
        self.in_dec_num = QtGui.QLabel(self.av_mon_in_group)
        self.in_dec_num.setObjectName("in_dec_num")
        self.gridLayout_8.addWidget(self.in_dec_num, 1, 11, 1, 1)
        self.gridLayout.addWidget(self.av_mon_in_group, 5, 0, 1, 4)

        #start monthly spend group
        self.av_mon_spend_group = QtGui.QGroupBox(Form)
        self.av_mon_spend_group.setObjectName("av_mon_spend_group")
        self.gridLayout_7 = QtGui.QGridLayout(self.av_mon_spend_group)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.spend_apr = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_apr.setObjectName("spend_apr")
        self.gridLayout_7.addWidget(self.spend_apr, 0, 3, 1, 1)
        self.spend_sep = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_sep.setObjectName("spend_sep")
        self.gridLayout_7.addWidget(self.spend_sep, 0, 8, 1, 1)
        self.spend_jun = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jun.setObjectName("spend_jun")
        self.gridLayout_7.addWidget(self.spend_jun, 0, 5, 1, 1)
        self.spend_jan_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jan_num.setObjectName("spend_jan_num")
        self.gridLayout_7.addWidget(self.spend_jan_num, 1, 0, 1, 1)
        self.spend_oct = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_oct.setObjectName("spend_oct")
        self.gridLayout_7.addWidget(self.spend_oct, 0, 9, 1, 1)
        self.spend_aug = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_aug.setObjectName("spend_aug")
        self.gridLayout_7.addWidget(self.spend_aug, 0, 7, 1, 1)
        self.spend_may = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_may.setObjectName("spend_may")
        self.gridLayout_7.addWidget(self.spend_may, 0, 4, 1, 1)
        self.spend_mar = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_mar.setObjectName("spend_mar")
        self.gridLayout_7.addWidget(self.spend_mar, 0, 2, 1, 1)
        self.spend_feb = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_feb.setObjectName("spend_feb")
        self.gridLayout_7.addWidget(self.spend_feb, 0, 1, 1, 1)
        self.spend_jan = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jan.setObjectName("spend_jan")
        self.gridLayout_7.addWidget(self.spend_jan, 0, 0, 1, 1)
        self.spend_jul = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jul.setObjectName("spend_jul")
        self.gridLayout_7.addWidget(self.spend_jul, 0, 6, 1, 1)
        self.spend_nov = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_nov.setObjectName("spend_nov")
        self.gridLayout_7.addWidget(self.spend_nov, 0, 10, 1, 1)
        self.spend_dec = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_dec.setObjectName("spend_dec")
        self.gridLayout_7.addWidget(self.spend_dec, 0, 11, 1, 1)
        self.spend_feb_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_feb_num.setObjectName("spend_feb_num")
        self.gridLayout_7.addWidget(self.spend_feb_num, 1, 1, 1, 1)
        self.spend_mar_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_mar_num.setObjectName("spend_mar_num")
        self.gridLayout_7.addWidget(self.spend_mar_num, 1, 2, 1, 1)
        self.spend_apr_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_apr_num.setObjectName("spend_apr_num")
        self.gridLayout_7.addWidget(self.spend_apr_num, 1, 3, 1, 1)
        self.spend_may_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_may_num.setObjectName("spend_may_num")
        self.gridLayout_7.addWidget(self.spend_may_num, 1, 4, 1, 1)
        self.spend_jun_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jun_num.setObjectName("spend_jun_num")
        self.gridLayout_7.addWidget(self.spend_jun_num, 1, 5, 1, 1)
        self.spend_jul_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_jul_num.setObjectName("spend_jul_num")
        self.gridLayout_7.addWidget(self.spend_jul_num, 1, 6, 1, 1)
        self.spend_aug_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_aug_num.setObjectName("spend_aug_num")
        self.gridLayout_7.addWidget(self.spend_aug_num, 1, 7, 1, 1)
        self.spend_sep_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_sep_num.setObjectName("spend_sep_num")
        self.gridLayout_7.addWidget(self.spend_sep_num, 1, 8, 1, 1)
        self.spend_oct_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_oct_num.setObjectName("spend_oct_num")
        self.gridLayout_7.addWidget(self.spend_oct_num, 1, 9, 1, 1)
        self.spend_nov_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_nov_num.setObjectName("spend_nov_num")
        self.gridLayout_7.addWidget(self.spend_nov_num, 1, 10, 1, 1)
        self.spend_dec_num = QtGui.QLabel(self.av_mon_spend_group)
        self.spend_dec_num.setObjectName("spend_dec_num")
        self.gridLayout_7.addWidget(self.spend_dec_num, 1, 11, 1, 1)
        self.gridLayout.addWidget(self.av_mon_spend_group, 3, 0, 1, 4)

        #start daily spend group
        self.av_day_spend_group = QtGui.QGroupBox(Form)
        self.av_day_spend_group.setObjectName("thu_spend")
        self.gridLayout_2 = QtGui.QGridLayout(self.av_day_spend_group)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.thu_spend = QtGui.QLabel(self.av_day_spend_group)
        self.thu_spend.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.thu_spend, 0, 3, 1, 1)
        self.wed_spend = QtGui.QLabel(self.av_day_spend_group)
        self.wed_spend.setObjectName("wed_spend")
        self.gridLayout_2.addWidget(self.wed_spend, 0, 2, 1, 1)
        self.sat_spend = QtGui.QLabel(self.av_day_spend_group)
        self.sat_spend.setObjectName("sat_spend")
        self.gridLayout_2.addWidget(self.sat_spend, 0, 5, 1, 1)
        self.sun_spend = QtGui.QLabel(self.av_day_spend_group)
        self.sun_spend.setObjectName("sun_spend")
        self.gridLayout_2.addWidget(self.sun_spend, 0, 6, 1, 1)
        self.fri_spend = QtGui.QLabel(self.av_day_spend_group)
        self.fri_spend.setObjectName("fri_spend")
        self.gridLayout_2.addWidget(self.fri_spend, 0, 4, 1, 1)
        self.tue_spend = QtGui.QLabel(self.av_day_spend_group)
        self.tue_spend.setTextFormat(QtCore.Qt.RichText)
        self.tue_spend.setObjectName("tue_spend")
        self.gridLayout_2.addWidget(self.tue_spend, 0, 1, 1, 1)
        self.mon_spend = QtGui.QLabel(self.av_day_spend_group)
        self.mon_spend.setTextFormat(QtCore.Qt.RichText)
        self.mon_spend.setObjectName("mon_spend")
        self.gridLayout_2.addWidget(self.mon_spend, 0, 0, 1, 1)
        self.mon_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.mon_spend_num.setObjectName("mon_spend_num")
        self.gridLayout_2.addWidget(self.mon_spend_num, 1, 0, 1, 1)
        self.tue_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.tue_spend_num.setObjectName("tue_spend_num")
        self.gridLayout_2.addWidget(self.tue_spend_num, 1, 1, 1, 1)
        self.wed_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.wed_spend_num.setObjectName("wed_spend_num")
        self.gridLayout_2.addWidget(self.wed_spend_num, 1, 2, 1, 1)
        self.thu_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.thu_spend_num.setObjectName("thu_spend_num")
        self.gridLayout_2.addWidget(self.thu_spend_num, 1, 3, 1, 1)
        self.fri_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.fri_spend_num.setObjectName("fri_spend_num")
        self.gridLayout_2.addWidget(self.fri_spend_num, 1, 4, 1, 1)
        self.sat_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.sat_spend_num.setObjectName("sat_spend_num")
        self.gridLayout_2.addWidget(self.sat_spend_num, 1, 5, 1, 1)
        self.sun_spend_num = QtGui.QLabel(self.av_day_spend_group)
        self.sun_spend_num.setObjectName("sun_spend_num")
        self.gridLayout_2.addWidget(self.sun_spend_num, 1, 6, 1, 1)
        self.gridLayout.addWidget(self.av_day_spend_group, 7, 0, 1, 4)


        #start account income group
        self.account_in_group = QtGui.QGroupBox(Form)
        self.account_in_group.setObjectName("account_in_group")
        self.gridLayout_3 = QtGui.QGridLayout(self.account_in_group)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout.addWidget(self.account_in_group, 8, 0, 1, 4)

        #start account spend group
        self.account_spend_group = QtGui.QGroupBox(Form)
        self.account_spend_group.setObjectName("account_spend_group")
        self.gridLayout_4 = QtGui.QGridLayout(self.account_spend_group)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout.addWidget(self.account_spend_group, 10, 0, 1, 4)

        #start type spend group
        self.type_spend_group = QtGui.QGroupBox(Form)
        self.type_spend_group.setObjectName("type_spend_group")
        self.gridLayout_6 = QtGui.QGridLayout(self.type_spend_group)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout.addWidget(self.type_spend_group, 12, 0, 1, 4)

        #start account net group
        self.account_net_group = QtGui.QGroupBox(Form)
        self.account_net_group.setObjectName("account_net_group")
        self.gridLayout_5 = QtGui.QGridLayout(self.account_net_group)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout.addWidget(self.account_net_group, 11, 0, 1, 4)

        #label setting - numbers

        self.loaded = get_all()

        self.months = {1:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_jan_num, self.spend_jan_num]},
                      2:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_feb_num, self.spend_feb_num]},
                      3:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_mar_num, self.spend_mar_num]},
                      4:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_apr_num, self.spend_apr_num]},
                      5:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_may_num, self.spend_may_num]},
                      6:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_jun_num, self.spend_jun_num]},
                      7:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_jul_num, self.spend_jul_num]},
                      8:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_aug_num, self.spend_aug_num]},
                      9:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_sep_num, self.spend_sep_num]},
                      10:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_oct_num, self.spend_oct_num]},
                      11:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_nov_num, self.spend_nov_num]},
                      12:{"in":Decimal(0), "out":Decimal(0), "obj":[self.in_dec_num, self.spend_dec_num]}}

        self.days = {0:{"in":Decimal(0), "out":Decimal(0), "obj":self.mon_spend_num, "num":0},
                    1:{"in":Decimal(0), "out":Decimal(0), "obj":self.tue_spend_num, "num":0},
                    2:{"in":Decimal(0), "out":Decimal(0), "obj":self.wed_spend_num, "num":0},
                    3:{"in":Decimal(0), "out":Decimal(0), "obj":self.thu_spend_num, "num":0},
                    4:{"in":Decimal(0), "out":Decimal(0), "obj":self.fri_spend_num, "num":0},
                    5:{"in":Decimal(0), "out":Decimal(0), "obj":self.sat_spend_num, "num":0},
                    6:{"in":Decimal(0), "out":Decimal(0), "obj":self.sun_spend_num, "num":0}}
        self.accounts = {}
        self.types = {}
        self.income = Decimal(0)
        self.spend = Decimal(0)
        self.net = Decimal(0)

        for date in self.loaded:
            self.days[date.weekday()]["num"] += 1
            for transaction in self.loaded[date].transactions:
                if transaction.amount <0:
                    self.months[date.month]["out"] += transaction.amount
                    self.days[date.weekday()]["out"] += transaction.amount

                    if not transaction.account in self.accounts:
                        self.accounts[transaction.account] = {"in":Decimal(0), "out":Decimal(0)}
                        self.accounts[transaction.account]["out"] = transaction.amount
                    else:
                        self.accounts[transaction.account]["out"] += transaction.amount

                    if not transaction.type in self.types:
                        self.types[transaction.type] = {"in":Decimal(0), "out":Decimal(0)}
                        self.types[transaction.type]["out"] = transaction.amount
                    else:
                        self.types[transaction.type]["out"] += transaction.amount

                    self.spend += transaction.amount

                else:
                    self.months[date.month]["in"] += transaction.amount
                    self.days[date.weekday()]["in"] += transaction.amount

                    if not transaction.account in self.accounts:
                        self.accounts[transaction.account] = {"in":Decimal(0), "out":Decimal(0)}
                        self.accounts[transaction.account]["in"] = transaction.amount
                    else:
                        self.accounts[transaction.account]["in"] += transaction.amount

                    if not transaction.type in self.types:
                        self.types[transaction.type] = {"in":Decimal(0), "out":Decimal(0)}
                        self.types[transaction.type]["in"] = transaction.amount
                    else:
                        self.types[transaction.type]["in"] += transaction.amount

                    self.income += transaction.amount


        TWOPLACES = Decimal(10) ** -2
        self.net = self.income + self.spend
        self.mon_in_av = 0
        self.mon_spend_av = 0
        self.mon_net_av = 0
        for month in self.months:
            self.months[month]["obj"][0].setText(str(self.months[month]["in"]))
            self.months[month]["obj"][1].setText(str(self.months[month]["out"]))
            self.mon_in_av += self.months[month]["in"]
            self.mon_spend_av += self.months[month]["out"]
            self.mon_net_av += self.months[month]["in"]
            self.mon_net_av += self.months[month]["out"]
        for day in self.days:
            self.days[day]["out"] = self.days[day]["out"]/self.days[day]["num"]
            self.days[day]["obj"].setText(str(self.days[day]["out"].quantize(TWOPLACES)))

        for type in enumerate(self.types):
            self.gridLayout_6.addWidget(QtGui.QLabel("<b>"+type[1]+"<\b>"), 0 , type[0])
            self.gridLayout_6.addWidget(QtGui.QLabel(str(self.types[type[1]]["out"]+self.types[type[1]]["in"])), 1, type[0])

        for type in enumerate(self.accounts):
            self.gridLayout_3.addWidget(QtGui.QLabel("<b>"+type[1]+"<\b>"), 0 , type[0])
            self.gridLayout_3.addWidget(QtGui.QLabel(str(self.accounts[type[1]]["in"])), 1, type[0])
            self.gridLayout_4.addWidget(QtGui.QLabel("<b>"+type[1]+"<\b>"), 0 , type[0])
            self.gridLayout_4.addWidget(QtGui.QLabel(str(self.accounts[type[1]]["out"])), 1, type[0])
            self.gridLayout_5.addWidget(QtGui.QLabel("<b>"+type[1]+"<\b>"), 0 , type[0])
            self.gridLayout_5.addWidget(QtGui.QLabel(str(self.accounts[type[1]]["out"]+self.accounts[type[1]]["in"])), 1, type[0])


        self.mon_in_av = Decimal(self.mon_in_av)/12
        self.mon_spend_av = Decimal(self.mon_spend_av)/12
        self.mon_net_av = Decimal(self.mon_net_av)/12

        self.tot_spend_num.setText(str(self.spend.quantize(TWOPLACES)))
        self.tot_in_num.setText(str(self.income.quantize(TWOPLACES)))
        self.net_in_num.setText(str(self.net.quantize(TWOPLACES)))


        self.av_mon_in_num.setText(str(self.mon_in_av.quantize(TWOPLACES)))
        self.av_mon_spend_num.setText(str(self.mon_spend_av.quantize(TWOPLACES)))
        self.av_mon_net_num.setText(str(self.mon_net_av.quantize(TWOPLACES)))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.av_mon_net.setText(QtGui.QApplication.translate("Form", "<b>Average monthly net:<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.tot_in.setText(QtGui.QApplication.translate("Form", "<b>Total income so far:<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.av_mon_in_group.setTitle(QtGui.QApplication.translate("Form", "Average income by month", None, QtGui.QApplication.UnicodeUTF8))
        self.in_jan.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jan</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_feb.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Feb</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_mar.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Mar</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_apr.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Apr</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_may.setText(QtGui.QApplication.translate("Form", "<b>May<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_jun.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jun</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_jul.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jul</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_aug.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Aug</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_sep.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Sep</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_oct.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Oct</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_nov.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Nov</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.in_dec.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Dec</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tot_spend.setText(QtGui.QApplication.translate("Form", "<b>Total spend so far:<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.av_mon_spend_group.setTitle(QtGui.QApplication.translate("Form", "Average spend by month", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_apr.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Apr</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_sep.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Sep</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_jun.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jun</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_oct.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Oct</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_aug.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Aug</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_may.setText(QtGui.QApplication.translate("Form", "<b>May<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_mar.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Mar</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_feb.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Feb</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_jan.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jan</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_jul.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Jul</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_nov.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Nov</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spend_dec.setText(QtGui.QApplication.translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Dec</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.av_day_spend_group.setTitle(QtGui.QApplication.translate("Form", "Average spend by day of the week", None, QtGui.QApplication.UnicodeUTF8))
        self.thu_spend.setText(QtGui.QApplication.translate("Form", "<b>Thursday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.wed_spend.setText(QtGui.QApplication.translate("Form", "<b>Wednesday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.sat_spend.setText(QtGui.QApplication.translate("Form", "<b>Saturday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.sun_spend.setText(QtGui.QApplication.translate("Form", "<b>Sunday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.fri_spend.setText(QtGui.QApplication.translate("Form", "<b>Friday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.tue_spend.setText(QtGui.QApplication.translate("Form", "<b>Tuesday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.mon_spend.setText(QtGui.QApplication.translate("Form", "<b>Monday<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.account_in_group.setTitle(QtGui.QApplication.translate("Form", "Income by account", None, QtGui.QApplication.UnicodeUTF8))
        self.account_spend_group.setTitle(QtGui.QApplication.translate("Form", "Spend by account", None, QtGui.QApplication.UnicodeUTF8))
        self.type_spend_group.setTitle(QtGui.QApplication.translate("Form", "Net by type", None, QtGui.QApplication.UnicodeUTF8))
        self.av_mon_in.setText(QtGui.QApplication.translate("Form", "<b>Average monthly income:<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.av_mon_spend.setText(QtGui.QApplication.translate("Form", "<b>Average monthly spend:<b>", None, QtGui.QApplication.UnicodeUTF8))
        self.account_net_group.setTitle(QtGui.QApplication.translate("Form", "Net by account", None, QtGui.QApplication.UnicodeUTF8))
        self.net_in.setText(QtGui.QApplication.translate("Form", "<b>Net income:<b>", None, QtGui.QApplication.UnicodeUTF8))


class TableView(object):
    def setupUi(self, tabs):
        self.accounts = {}
        self.accounts2 = []
        self.types = {}
        for account in listdir("../core/accounts"):
            self.accounts[account.replace(".pkl", "")] = []
            self.accounts2.append(account.replace(".pkl", ""))
        for typ in listdir("../core/types"):
            self.types[typ.replace(".pkl", "")] = []


        tabs.setObjectName("tabs")
        tabs.resize(1020, 1250)
        self.gridLayout_main = QtGui.QGridLayout(tabs)
        self.tabs = QtGui.QTabWidget(tabs)
        self.tabs.setTabPosition(QtGui.QTabWidget.North)
        self.tabs.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabs.setMovable(True)

        self.keylist, self.numDict = list_grabber()
        self.data = get_all()
        self.dates = list(self.data.keys())
        self.dates.sort()

        self.name_num = {}
        self.type_num = {}
        self.date_names = []
        self.nam_names = {}
        self.typ_names = list(self.numDict.keys())

        for typ in self.numDict:
            self.type_num[typ] = [0] * (self.numDict[typ]+1)
            self.nam_names[typ] = [0] * (self.numDict[typ]+1)

        for date in self.dates:
            day = str(date.year)+"/"
            if len(str(date.month)) == 1:
                day += "0"+str(date.month)+"/"
            else:
                day += str(date.month)+"/"
            if len(str(date.day)) == 1:
                day += "0"+str(date.day)
            else:
                day += str(date.day)
            self.date_names.append(day)

        for name in self.keylist:
            self.nam_names[self.keylist[name][0]][self.keylist[name][1]] = name

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.sum_table = QtGui.QTableWidget(self.tab)
        self.sum_table.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.sum_table.setObjectName("sum_table")
        self.sum_table.setColumnCount(len(self.accounts))
        self.sum_table.setHorizontalHeaderLabels(self.accounts2)
        self.sum_table.setRowCount(len(self.dates))
        self.sum_table.setVerticalHeaderLabels(self.date_names)
        self.gridLayout.addWidget(self.sum_table, 0, 0, 1, 1)
        self.tabs.addTab(self.tab, "")

        #for col in range(len(self.accounts2)):
         #   for row in range (len(self.dates)):
          #      self.sum_table.setItem(row, col, QtGui.QTableWidgetItem("0"))

        for account in self.accounts:
            self.accounts[account].append(QtGui.QWidget())
            self.accounts[account].append(QtGui.QGridLayout(self.accounts[account][0]))
            self.accounts[account].append(QtGui.QTableWidget(self.accounts[account][0]))
            self.accounts[account][2].setColumnCount(len(self.numDict))
            self.accounts[account][2].setHorizontalHeaderLabels(self.typ_names)
            self.accounts[account][2].setRowCount(len(self.dates))
            self.accounts[account][2].setVerticalHeaderLabels(self.date_names)
            self.accounts[account][1].addWidget(self.accounts[account][2], 0, 0, 1, 1)
            self.tabs.addTab(self.accounts[account][0], "")
            self.tabs.setTabText(self.tabs.indexOf(self.accounts[account][0]), account)

            #for col in range(len(self.numDict)):
             #   for row in range (len(self.dates)):
              #      self.accounts[account][2].setItem(row, col, QtGui.QTableWidgetItem("0"))

        for typ in self.types:
            self.types[typ].append(QtGui.QWidget())
            self.types[typ].append(QtGui.QGridLayout(self.types[typ][0]))
            self.types[typ].append(QtGui.QTableWidget(self.types[typ][0]))
            self.types[typ][2].setColumnCount(self.numDict[typ])
            self.types[typ][2].setHorizontalHeaderLabels(self.nam_names[typ])
            self.types[typ][2].setRowCount(len(self.dates))
            self.types[typ][2].setVerticalHeaderLabels(self.date_names)
            self.types[typ][1].addWidget(self.types[typ][2], 0, 0, 1, 1)
            self.tabs.addTab(self.types[typ][0], "")
            self.tabs.setTabText(self.tabs.indexOf(self.types[typ][0]), typ)

            #for col in range(self.numDict[typ]):
             #   for row in range (len(self.dates)):
              #      self.types[typ][2].setItem(row, col, QtGui.QTableWidgetItem("0"))

        for date in enumerate(self.dates):
            for total in self.data[date[1]].name_totals:
                item = QtGui.QTableWidgetItem(str(self.data[date[1]].name_totals[total]))
                self.types[self.keylist[total][0]][2].setItem(date[0], self.keylist[total][1], item)


            for account in self.data[date[1]].account_totals:
                running_total = 0
                for typ in self.data[date[1]].account_totals[account]:
                    num = self.data[date[1]].account_totals[account][typ]
                    item = QtGui.QTableWidgetItem(str(num))
                    self.accounts[account][2].setItem(date[0], self.typ_names.index(typ),item)
                    running_total += num
                running_total = QtGui.QTableWidgetItem(str(running_total))
                self.sum_table.setItem(date[0], self.accounts2.index(account), running_total)

        self.sum_table.resizeColumnsToContents()

        for account in self.accounts:
            self.accounts[account][2].resizeColumnsToContents()

        for typ in self.types:
            self.types[typ][2].resizeColumnsToContents()

        self.retranslateUi(tabs)
        self.tabs.setCurrentIndex(0)
        self.gridLayout_main.addWidget(self.tabs, 0, 0)
        QtCore.QMetaObject.connectSlotsByName(tabs)

    def retranslateUi(self, tabs):
        tabs.setWindowTitle(QtGui.QApplication.translate("tabs", "TabWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), QtGui.QApplication.translate("tabs", "Summary", None, QtGui.QApplication.UnicodeUTF8))
        #tabs.setTabText(tabs.indexOf(self.tab1), QtGui.QApplication.translate("tabs", "Account 1", None, QtGui.QApplication.UnicodeUTF8))
        #tabs.setTabText(tabs.indexOf(self.tab_2), QtGui.QApplication.translate("tabs", "Type 1", None, QtGui.QApplication.UnicodeUTF8))

class GraphicalCanvas(FigureCanvas):
    def __init__(self):
        #self.fig = Figure()
        #self.ax = self.fig.add_subplot(111)

        self.fig, self.ax  = plt.subplots()

        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class mplWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = GraphicalCanvas()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

class GraphicalView(QtGui.QWidget):
    def setupUi(self, widget):

        widget.setObjectName("graph")
        widget.resize(1200, 1250)

        self.gridLayout = QtGui.QGridLayout(widget)

        self.canvas = mplWidget(self)


        self.toolbar = NavigationToolbar(self.canvas.canvas, self)
        self.toolbar.hide()

        # Just some button

        self.button1 = QtGui.QPushButton('Zoom')
        self.button1.clicked.connect(self.zoom)

        self.button2 = QtGui.QPushButton('Pan')
        self.button2.clicked.connect(self.pan)

        self.button3 = QtGui.QPushButton('Home')
        self.button3.clicked.connect(self.home)


        # set the layout
        self.buttons = QtGui.QWidget(widget)
        self.buttons.resize(100,200)
        layout = QtGui.QVBoxLayout(self.buttons)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.plot("line")

        self.gridLayout.addWidget(self.canvas, 0 , 0, 1, 1)
        self.gridLayout.addWidget(self.buttons, 1, 0, 1, 1)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def home(self):
        self.toolbar.home()
    def zoom(self):
        self.toolbar.zoom()
    def pan(self):
        self.toolbar.pan()

    def plot(self, graph_type):
        ''' plot some random stuff '''
        self.data = get_all()
        self.axis = {}

        '''for date in self.data:

            if not str(date.year)+"-"+str(date.month) in self.axis:
                self.axis[str(date.year)+"-"+str(date.month)] = 0

            self.axis[str(date.year)+"-"+str(date.month)] += self.data[date].total'''

        for date in self.data:
            key = datetime.datetime(date.year, date.month, 1,0,0)
            if not key in self.axis:
                self.axis[key] = 0

            self.axis[key] += self.data[date].total

        self.x = list(self.axis.keys())
        self.x.sort()
        self.y = []
        #print(self.x)
        for key in self.x:
            self.y.append(self.axis[key])

        self.canvas.canvas.ax.clear()
        if graph_type == "line":

            self.canvas.canvas.ax.plot(self.x, self.y)
            self.canvas.canvas.ax.xaxis_date()
            self.canvas.canvas.ax.grid()
            #ax = self.figure.add_subplot(111)
            #ax.hold(False)
            #ax.plot(range(len(self.x)), self.y)
        elif graph_type == "bar":
            self.canvas.canvas.ax.bar(self.x, self.y, width = 20, edgecolor="black", align="center")
            #self.canvas.canvas.ax.xaxis.set_ticks(np.arange(len(self.x)))
            self.canvas.canvas.ax.xaxis_date()
            #self.canvas.canvas.ax.set_xticklabels(self.x, rotation = 20)
            self.canvas.canvas.ax.grid()

        self.canvas.canvas.draw()

#///////////////////////////////////////////// End Central Widget classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#///////////////////////////////////////////// Start Main Window classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
class Ui_MainWindow(object):
    def __init__(self, some_func, accounts):
        self.some_func = some_func
        self.accounts = accounts
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExport_To = QtGui.QMenu(self.menuFile)
        self.menuExport_To.setObjectName("menuExport_To")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionCSV = QtGui.QAction(MainWindow)
        self.actionCSV.setObjectName("actionCSV")
        self.actionXML = QtGui.QAction(MainWindow)
        self.actionXML.setObjectName("actionXML")
        self.actionSQL = QtGui.QAction(MainWindow)
        self.actionSQL.setObjectName("actionSQL")
        self.actionCreate_Account = QtGui.QAction(MainWindow)
        self.actionCreate_Account.setObjectName("actionCreate_Account")
        self.actionCreate_Type = QtGui.QAction(MainWindow)
        self.actionCreate_Type.setObjectName("actionCreate_Type")
        self.actionCreate_Group = QtGui.QAction(MainWindow)
        self.actionCreate_Group.setObjectName("actionCreate_Group")
        self.actionChange_List_Order = QtGui.QAction(MainWindow)
        self.actionChange_List_Order.setObjectName("actionChange_List_Order")
        self.actionAbout_PyFi = QtGui.QAction(MainWindow)
        self.actionAbout_PyFi.setObjectName("actionAbout_PyFi")
        self.menuExport_To.addAction(self.actionCSV)
        self.menuExport_To.addAction(self.actionXML)
        self.menuExport_To.addAction(self.actionSQL)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.menuExport_To.menuAction())
        self.menuTools.addAction(self.actionCreate_Account)
        self.menuTools.addAction(self.actionCreate_Type)
        self.menuTools.addAction(self.actionCreate_Group)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionChange_List_Order)
        self.menuHelp.addAction(self.actionAbout_PyFi)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.actionCreate_Account.triggered.connect(self.popup_account)
        self.actionCreate_Type.triggered.connect(self.popup_type)
        self.actionCSV.triggered.connect(self.write_csvs)
        self.actionImport.triggered.connect(self.popup_statement)

    def popup_statement(self):
        from main import start
        self.pops = DialogWidg('Statement', accounts=self.accounts)
        if self.pops.exec_():
            account, filepath = self.pops.widg.get_values()
            start(statement_file = filepath, account = account)

    def popup_type(self):
        self.pops = DialogWidg('Type')
        self.pops.exec_()

    def popup_account(self):
        self.pops = DialogWidg('Account')
        self.pops.exec_()

    def write_csvs(self):
        #print(1)
        beginning, end, types, accounts = self.find_filters()

        self.some_func(False, beginning, end, types, accounts)
        #print(2)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuExport_To.setTitle(QtGui.QApplication.translate("MainWindow", "Export To...", None,
                                                                 QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None,
                                                             QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("MainWindow", "Import...", None,
                                                               QtGui.QApplication.UnicodeUTF8))
        self.actionCSV.setText(QtGui.QApplication.translate("MainWindow", "CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.actionXML.setText(QtGui.QApplication.translate("MainWindow", "XML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSQL.setText(QtGui.QApplication.translate("MainWindow", "SQL", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCreate_Account.setText(QtGui.QApplication.translate("MainWindow", "Create Account", None,
                                                                       QtGui.QApplication.UnicodeUTF8))
        self.actionCreate_Type.setText(QtGui.QApplication.translate("MainWindow", "Create Type", None,
                                                                    QtGui.QApplication.UnicodeUTF8))
        self.actionCreate_Group.setText(QtGui.QApplication.translate("MainWindow", "Create Group", None,
                                                                     QtGui.QApplication.UnicodeUTF8))
        self.actionChange_List_Order.setText(QtGui.QApplication.translate("MainWindow", "Change List Order",
                                                                          None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_PyFi.setText(QtGui.QApplication.translate("MainWindow", "About PyFi", None,
                                                                   QtGui.QApplication.UnicodeUTF8))

#///////////////////////////////////////////// End Main Window classes.py \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
