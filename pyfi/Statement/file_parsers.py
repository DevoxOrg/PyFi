import csv
import datetime
import decimal

from pyfi.db.models import Transaction
from pyfi.db.session import create_session

class NotImplementedError(Exception):
    pass

class BaseParser:
    """
    We need individual parsers to deal with different bank formats.

    They all need some common functionality so will inherit from this base class.

    Initial requirements are to create the data fields to insert into and call the parse function which parses the file.

    All parsers should result in the same output so we can then have the insert_into_db method.
    """
    def __init__(self, filepath, account=None):
        """
        Initialiser for Base_Parser

        :param filepath: str, the filepath for the
        :return: None
        """
        if account is None:
            raise NotImplementedError("Account is None! Can't insert transactions into nothing!")

        self.account = account

        self.transactions = []
        self.file = filepath

        self.parse()

        self.insert_into_db()

    def parse(self):
        raise NotImplementedError('Parse function is not implemented for this parser!')

    def insert_into_db(self):
        """
        Take the transactions stored in this parser, calculate them, and insert them into db.

        :return: None
        """

        for transaction in self.transactions:
            transaction.calculate_type()

        session = create_session()
        session.add_all(self.transactions)
        session.commit()


class HSBCParser(BaseParser):

    def parse(self):
        """
        Method to parse HSBC statements and create data for the db.

        :return: None
        """

        with open(self.file, 'r') as statement:
            reader = csv.reader(statement)
            for row in reader:
                day = datetime.datetime.strptime(row[0], '%Y-%m-%d')
                name = row[1]
                amount = decimal.Decimal(row[2])

                transaction = Transaction(date=day,
                                          true_name=name,
                                          amount=amount,
                                          account=self.account)

                self.transactions.append(transaction)

class HalifaxParser(BaseParser):

    def parse(self):
        """
        Method to parse Halifax statements and create data for the db

        :return: None
        """

        with open(self.file, 'r') as statement:
            reader = csv.reader(statement)
            reader.__next__()

            for row in reader:

                day = datetime.datetime.strptime(row[0], '%d/%m/%Y')

                if row[5]:
                    amount = -decimal.Decimal(row[5])
                elif row[6]:
                    amount = decimal.Decimal(row[6])
                else:
                    raise NotImplementedError("No transaction amount!")

                name = row[4]

                transaction = Transaction(date=day,
                                          true_name=name,
                                          amount=amount,
                                          account=self.account)

                self.transactions.append(transaction)