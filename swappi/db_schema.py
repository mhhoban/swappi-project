from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    title = Column(String(50), nullable=False)
    description = Column(String(250))
    poster_id = Column(Integer, ForeignKey('users.id'))
    poster = relationship(Users)
    swap_for = Column(String(100), nullable=False)


engine = create_engine('sqlite:///db/itemcatalog.db')

Base.metadata.create_all(engine)