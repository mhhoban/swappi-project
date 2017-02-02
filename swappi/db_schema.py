import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """
        Return user data in serializable format
        """

        return {
            'id': self.id,
            'name': self.name,
        }

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    @property
    def serialize(self):
        """
        Return Category Data in serializable format
        :return:
        """

        return {
            'id': self.id,
            'name': self.name,
        }

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    title = Column(String(50), nullable=False)
    description = Column(String(250))

    @property
    def serialize(self):
        """
        return item data in serializable format
        """

        return {
            'id': self.id,
            'category_id': self.category_id,
            'category': self.category,
            'title': self.title,
            'description': self.description,
        }



engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.create_all(engine)