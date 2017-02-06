from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users

import db_setup


app = Flask(__name__)
app.config['SQL_DB_URI'] = 'sqlite:///db/itemcatalog.db'


# # TODO: move db init to setup.py
# def db_init():
#     _db_setup = db_setup.DbSetup(app.config['SQL_DB_URI'])
#     _db_setup.db_init()


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
    category_name = (session.query(Categories).filter_by(id=category_id).one()).name
    categories = session.query(Categories).all()
    items = session.query(Items).filter_by(category_id=category_id).all()

    return render_template('categories.html',
                           category_name=category_name,
                           categories=categories,
                           items=items,
                           )

@app.route('/item/<int:item_id>')
def item_page(item_id):

    session = get_db_cursor()
    item_data = session.query(Items).filter_by(id=item_id).one()

    item_category = item_data.category.name
    item_title = item_data.title
    item_desc = item_data.description

    categories = session.query(Categories).all()
    items = session.query(Items).filter_by(category_id=item_data.category_id).all()

    return render_template('items.html',
                           item_cat=item_category,
                           item_title=item_title,
                           item_desc=item_desc,
                           categories=categories,
                           items=items,
                           )


@app.route('/add-item', methods=['GET', 'POST'])
def item_add():

    session = get_db_cursor()

    if request.method == 'POST':
        item_title = request.form['item_title']
        item_desc = request.form['item_desc']
        item_cat = request.form['item_cat']

        newItem = Items(title=item_title,
                        description=item_desc,
                        category_id=int(item_cat),
                        )
        session.add(newItem)
        session.commit()

        return redirect(url_for('indexPage'))

    else:

        categories = session.query(Categories).all()

        return render_template('add.html',
                               categories=categories,
                               )


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=8080)
