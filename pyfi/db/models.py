from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///../../foo.db', echo=True)

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)

    bank = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)

    transactions = relationship("Transaction")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

    amount = Column(Numeric(18, 2), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)

print()

Base.metadata.create_all(engine)