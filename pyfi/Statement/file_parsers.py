import csv

from pyfi.db.session import create_session
from pyfi.db.models import Transaction

class base_parser:
    """
    We need individual parsers to deal with different bank formats.

    They all need some common functionality so will inherit from this base class.

    Initial requirements are to create the data fields to insert into and call the parse function which parses the file.

    All parsers should result in the same output so we can then have the insert_into_db method.
    """
    def __init__(self, filepath):
        self.transactions = ()
        self.file = filepath

        self.parse(self.file)

        self.insert_into_db()

    def parse(self, filepath):
        pass

    def insert_into_db(self):
        session = create_session()
        session.add_all(self.transactions)
        session.commit()