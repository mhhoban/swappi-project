from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users
from oauth2client import client, crypt

import json

from flask import make_response
import requests

import random
import string
import user_utils

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Swappi"

app.config['SQL_DB_URI'] = 'sqlite:///db/itemcatalog.db'


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


@app.route('/auth', methods=['GET', 'POST'])
def authorization():

    print('in auth func')

    gtoken = request.values['idtoken']
    login_email = False

    try:
        idinfo = client.verify_id_token(gtoken, CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

        else:
            login_email = idinfo['email']

    except crypt.AppIdentityError:

        raise

    if login_email:

        user_data = user_utils.check_user_exists(get_db_cursor(), login_email)

        if user_data:
            login_session['user_email'] = user_data['email']
            login_session['name'] = user_data['name']
            login_session['user_id'] = user_data['id']

        else:

            user_utils.register_new_user(idinfo['name'], idinfo['email'], get_db_cursor())

        return make_response('valid')

    else:
        return make_response('invalid')


@app.route('/deauth', methods=['GET', 'POST'])
def deauthorization():

    if request.values['logout'] == 'True':

        try:
            del login_session['user_email']
            del login_session['name']
            del login_session['user_id']

            return make_response('success')

        except KeyError:

            return make_response('not logged in')


@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']

    return render_template('login.html')


@app.route('/')
def indexPage():

    session = get_db_cursor()
    categories = session.query(Categories).all()
    items = session.query(Items).all()

    user = user_utils.user_auth_check(login_session)

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           user=user,
                           )


@app.route('/category/<int:category_id>')
def category_page(category_id):

    user = user_utils.user_auth_check(login_session)

    session = get_db_cursor()
    category_name = (session.query(Categories).filter_by(id=category_id).one()).name
    categories = session.query(Categories).all()
    items = session.query(Items).filter_by(category_id=category_id).all()

    return render_template('categories.html',
                           category_name=category_name,
                           categories=categories,
                           items=items,
                           user=user,
                           )


@app.route('/item/<int:item_id>')
def item_page(item_id):

    user = user_utils.user_auth_check(login_session)

    session = get_db_cursor()
    item_data = session.query(Items).filter_by(id=item_id).one()

    item_category = item_data.category.name
    item_title = item_data.title
    item_desc = item_data.description
    item_poster = item_data.poster.name

    categories = session.query(Categories).all()
    items = session.query(Items).filter_by(category_id=item_data.category_id).all()

    return render_template('items.html',
                           item_cat=item_category,
                           item_title=item_title,
                           item_desc=item_desc,
                           categories=categories,
                           items=items,
                           item_poster=item_poster,
                           user=user,
                           )


@app.route('/add-listing', methods=['GET', 'POST'])
def item_add():

    # check that user is signed in:
    user = user_utils.user_auth_check(login_session)
    if user:
        session = get_db_cursor()
        if request.method == 'POST':
            item_title = request.form['item_title']
            item_desc = request.form['item_desc']
            item_cat = request.form['item_cat']
            item_poster = login_session['user_id']

            newItem = Items(title=item_title,
                            description=item_desc,
                            category_id=int(item_cat),
                            poster_id=item_poster,
                            )
            session.add(newItem)
            session.commit()

            return redirect(url_for('indexPage'))

        else:

            categories = session.query(Categories).all()
            user = user_utils.user_auth_check(login_session)

            return render_template('add.html',
                                   categories=categories,
                                   user=user,
                                   )
    else:
        return redirect(url_for('indexPage'))


@app.route('/view-listings', methods=['GET', 'POST'])
def view_item_listings():

    user = user_utils.user_auth_check(login_session)
    if user:
        session = get_db_cursor()

        if request.method == 'GET':
            poster_id = login_session['user_id']
            items = session.query(Items).filter_by(poster_id=poster_id)
            return render_template('view_listings.html',
                                   items=items,
                                   user=user)

    else:
        return redirect(url_for('indexPage'))



if __name__ == '__main__':
    app.secret_key = 'totally_secure'
    app.debug = True
    app.run(host='localhost', port=8080)
