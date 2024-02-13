import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = os.environ.get('DATABASE_URI')
engine = create_engine("{}".format(DATABASE_URI))

Base = declarative_base()

def get_session():
    Session = sessionmaker(engine)
    return Session()

def save_objeto(objeto, s):
    try:
        s.add(objeto)
        s.commit()
    except Exception as e:
        s.rollback()
        raise e