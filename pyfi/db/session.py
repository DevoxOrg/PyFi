from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import models

_ENGINE = create_engine('sqlite:///../../foo.db', echo=True)

_SESSION = sessionmaker(bind=_ENGINE)
