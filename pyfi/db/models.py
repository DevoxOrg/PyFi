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

    bank = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)

    transactions = relationship("Transaction")


class Transaction(_BASE):
    """
    Class representing the table holding all transactions.

    Holds multiple pieces of data representing what a transaction is.
    """
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)

    account = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    type = Column(String, ForeignKey('types.id'), nullable=False)

    # Some transactions add useless data on to the name. We remove this.
    # So store original name as true_name and used name as name.
    true_name = Column(String, nullable=False)
    name = Column(String, ForeignKey('ref_types_to_names.id'), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)
    date = Column(Date, nullable=False)


class Transaction_Type(_BASE):
    """
    Class representing the Types table holding all the possible types we currently have.
    """
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    type_name = Column(String, nullable=False)


class Name_To_Type(_BASE):
    """
    This Class represents a reference table for describing which type of transaction a name falls under.
    Using this means we don't have to continually input the type a transaction is.
    """
    __tablename__ = 'ref_types_to_names'

    name = Column(String, nullable=False, primary_key=True)
    type_id = Column(String, ForeignKey('types.id'), nullable=False)


class Name_Patterns(_BASE):
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

if __name__ == '__main__':
    engine = create_engine('sqlite:///../../foo.db', echo=True)
    _BASE.metadata.create_all(engine)
