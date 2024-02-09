from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:123456@db:3306/banco")

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