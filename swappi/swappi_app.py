from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users

import db_setup


app = Flask(__name__)
app.config['SQL_DB_URI'] = 'sqlite:///db/itemcatalog.db'
engine = create_engine(app.config['SQL_DB_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def db_init():
    _db_setup = db_setup.DbSetup(app.config['SQL_DB_URI'])
    _db_setup.db_init()


@app.route('/')
def helloWorld():

    categories = session.query(Categories).all()
    items = session.query(Items).all()

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           )

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080)
