from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_ENGINE = create_engine('sqlite:///../../foo.db', echo=True)

def create_session(engine=_ENGINE):
    session = sessionmaker(bind=engine)
    return session
