from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users

import db_setup


app = Flask(__name__)
app.config['SQL_DB_URI'] = 'sqlite:///db/itemcatalog.db'


# TODO: move db init to setup.py
def db_init():
    _db_setup = db_setup.DbSetup(app.config['SQL_DB_URI'])
    _db_setup.db_init()


def get_db_cursor():
    """
    creates and returns the DBsession
    :return:
    """

    engine = create_engine(app.config['SQL_DB_URI'])
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session


@app.route('/')
def indexPage():

    session = get_db_cursor()
    categories = session.query(Categories).all()
    items = session.query(Items).all()

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           )


@app.route('/category/<int:category_id>')
def category_page(category_id):

    session = get_db_cursor()
    category_name = (session.query(Categories).filter_by(category_id=category_id).one()).name
    categories = session.query(Categories).all()
    items = session.query(Items).filter_by(category_id=category_id).all()

    return render_template('categories.html',
                           category_name=category_name,
                           categories=categories,
                           items=items,
                           )

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080)
