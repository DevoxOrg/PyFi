import re

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

_BASE = declarative_base()


class Account(_BASE):
    """
    Class representing the table holding the accounts used in this program.
    """
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)

    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    account_holder = Column(String, nullable=False)
    date_opened = Column(Date, nullable=True)

    transactions = relationship('Transaction', back_populates='account')


class Transaction(_BASE):
    """
    Class representing the table holding all transactions.

    Holds multiple pieces of data representing what a transaction is.
    """
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship('Account', back_populates='transactions')

    type = Column(Integer, ForeignKey('types.id'), nullable=False)

    # Some transactions add useless data on to the name. We remove this.
    # So store original name as true_name and used name as name.
    true_name = Column(String, nullable=False)
    name = Column(String, ForeignKey('ref_types_to_names.id'), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)
    date = Column(Date, nullable=False)

    def calculate_type(self):
        """
        Transaction names and types aren't so simple.

        We need to find out the standard name for a transaction, using a list of regexes.

        We also need to find the type of a transaction through the then assigned name.

        :return: None
        """
        from db.session import create_session

        session = create_session()

        for row in session.query(NamePatterns):
            if re.match(row.pattern, self.true_name):
                self.name = row.name
                break
        else:
            self.name = self.true_name

        self.type = session.query(NameToType).filter_by(name=self.name).one()


class TransactionType(_BASE):
    """
    Class representing the Types table holding all the possible types we currently have.
    """
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type_name = Column(String, nullable=False)


class NameToType(_BASE):
    """
    This Class represents a reference table for describing which type of transaction a name falls under.
    Using this means we don't have to continually input the type a transaction is.
    """
    __tablename__ = 'ref_types_to_names'

    name = Column(String, nullable=False, primary_key=True)
    type_id = Column(Integer, ForeignKey('types.id'), nullable=False)


class NamePatterns(_BASE):
    """
    Class to hold all the regex patterns for generic names.

    This is useful for transactions which have extra data in the name, such as dates, or for chain stores,
    location data.

    We can use regex's to describe patterns, this can then be looped through and compared - if a pattern is found we
    will produce a more generic name to be used for the future. The true name with extra data is still kept,
    but it won't be used as much.
    """
    __tablename__ = 'name_patterns'

    pattern = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)


class Bank(_BASE):
    __table__name = 'banks'

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    parser = Column

def main():
    engine = create_engine('sqlite:///../../foo.db', echo=True)
    _BASE.metadata.create_all(engine)

if __name__ == '__main__':
    main()
