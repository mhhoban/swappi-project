from db_schema import Base, Categories, Items
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine
from oauth2client import client, crypt
from sqlalchemy.orm import sessionmaker


import json
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


def check_item_exists(item_id):
    """
    checks whether the specified item exists before trying to load it.
    :param item_id:
    :return: True/False
    """

    session = get_db_cursor()

    try:
        item = session.query(Items).filter_by(id=item_id).one()
        return True
    except ValueError:
        return False


def check_category_exists(cat_id):
    """
    checks whether the specified category exists before trying to load it.
    :param item_id:
    :return: True/False
    """

    session = get_db_cursor()

    try:
        cat = session.query(Categories).filter_by(id=cat_id).one()
        return True
    except ValueError:
        return False


@app.route('/auth', methods=['GET', 'POST'])
def authorization():
    """
    Handles authorizing a user based on the data received from Google.
    :return:
    """

    print('in auth func')

    gtoken = request.values['idtoken']
    login_email = False

    try:
        idinfo = client.verify_id_token(gtoken, CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com',
                                 'https://accounts.google.com']:
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

            user_utils.register_new_user(idinfo['name'], idinfo['email'],
                                         get_db_cursor())

        return make_response('valid')

    else:
        return make_response('invalid')


@app.route('/deauth', methods=['GET', 'POST'])
def deauthorization():
    """
    Logs a user out of the system.
    :return:
    """

    if request.values['logout'] == 'True':

        try:
            del login_session['user_email']
            del login_session['name']
            del login_session['user_id']

            return make_response('success')

        except KeyError:

            return make_response('not logged in')


@app.route('/')
def indexPage():
    """
    Displays main index page.
    :return:
    """

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
    """
    displays list of items within selected category.
    :param category_id:
    :return:
    """

    category_exists = check_category_exists(category_id)

    if category_exists:

        user = user_utils.user_auth_check(login_session)

        session = get_db_cursor()
        category_name = (session.query(Categories).filter_by(
            id=category_id).one()).name
        categories = session.query(Categories).all()
        items = session.query(Items).filter_by(
            category_id=category_id).all()

        return render_template('categories.html',
                               category_name=category_name,
                               categories=categories,
                               items=items,
                               user=user,
                               )

    else:
        return redirect(url_for('indexPage'))


@app.route('/item/<int:item_id>')
def item_page(item_id):
    """
    displays all categories, items within selected category,
    and the information about the selected item.
    :param item_id:
    :return:
    """

    item_exists = check_item_exists(item_id)

    if item_exists:

        user = user_utils.user_auth_check(login_session)
        owner = user_utils.user_owner_check(user, item_id, get_db_cursor())

        session = get_db_cursor()
        item_data = session.query(Items).filter_by(id=item_id).one()

        item_id = item_data.id
        item_category = item_data.category.name
        item_title = item_data.title
        item_desc = item_data.description
        item_poster = item_data.poster.name
        swap_for = item_data.swap_for

        categories = session.query(Categories).all()
        items = session.query(Items).filter_by(
            category_id=item_data.category_id).all()

        return render_template('items.html',
                               item_id=item_id,
                               item_cat=item_category,
                               item_title=item_title,
                               item_desc=item_desc,
                               categories=categories,
                               items=items,
                               item_poster=item_poster,
                               user=user,
                               swap_for=swap_for,
                               owner=owner,
                               )

    else:
        return redirect(url_for('indexPage'))


@app.route('/add-listing', methods=['GET', 'POST'])
def item_add():
    """
    lets logged in user add new items to the item databse.
    :return:
    """

    # check that user is signed in:
    user = user_utils.user_auth_check(login_session)

    if user:
        session = get_db_cursor()

        if request.method == 'POST':

            item_title = request.form['item_title']
            item_desc = request.form['item_desc']
            item_cat = request.form['item_cat']
            item_swap = request.form['swap_item_for']
            item_poster = login_session['user_id']

            newItem = Items(title=item_title,
                            description=item_desc,
                            category_id=int(item_cat),
                            poster_id=item_poster,
                            swap_for=item_swap,
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
    """
    returns list of all items a user has posted with
    options to edit or delete each one.
    :return:
    """

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


@app.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    lets user edit an item they have posted.
    :param item_id:
    :return:
    """

    user = user_utils.user_auth_check(login_session)
    if user:

        owner = user_utils.user_owner_check(user, item_id, get_db_cursor())
        if owner:

            session = get_db_cursor()

            if request.method == 'POST':

                try:
                    item = session.query(Items).filter_by(id=item_id).one()

                    u_item_title = request.form['item_title']
                    u_item_cat = request.form['item_cat']
                    u_item_desc = request.form['item_desc']
                    u_item_swap = request.form['swap_item_for']

                    update = session.query(Items).filter(Items.id == item_id).\
                        update({Items.title: u_item_title,
                                Items.category_id: u_item_cat,
                                Items.description: u_item_desc,
                                Items.swap_for: u_item_swap},
                               synchronize_session=False)

                    session.commit()

                    return redirect(url_for('indexPage'))

                except ValueError:
                    return redirect(url_for('indexPage'))

            else:

                try:
                    item = session.query(Items).filter_by(id=item_id).one()
                    categories = session.query(Categories).all()
                except ValueError:
                    return redirect(url_for('indexPage'))

                if item.poster_id == login_session['user_id']:

                    return render_template('item_edit.html',
                                           user=user,
                                           categories=categories,
                                           item=item,
                                           )

                else:
                    return redirect(url_for('indexPage'))

        else:
            # if ownership is rejected
            return redirect(url_for('indexPage'))

    else:
        return redirect(url_for('indexPage'))


@app.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    """
    lets user delete an item they have posted.
    :param item_id:
    :return:
    """

    user = user_utils.user_auth_check(login_session)
    if user:

        owner = user_utils.user_owner_check(user, item_id, get_db_cursor())

        if owner:

            session = get_db_cursor()

            if request.method == 'POST':

                if request.form['action'] == 'terminate':

                    try:
                        item_exists = session.query(Items).filter_by(
                            id=item_id).one()
                        delete = session.query(Items).filter_by(
                            id=item_id).delete(synchronize_session=False)
                        session.commit()

                        return redirect(url_for('indexPage'))

                    except ValueError:
                        return redirect(url_for('indexPage'))

                else:
                    return redirect(url_for('indexPage'))

            else:

                try:
                    item = session.query(Items).filter_by(id=item_id).one()
                except ValueError:
                    return redirect(url_for('indexPage'))

                if item.poster_id == login_session['user_id']:

                    return render_template('item_delete.html',
                                           user=user,
                                           item=item,
                                           )

                else:
                    return redirect(url_for('indexPage'))

        else:
            # if ownership is rejected
            return redirect(url_for('indexPage'))

    else:
        return redirect(url_for('indexPage'))


if __name__ == '__main__':
    app.secret_key = 'totally_secure'
    app.debug = True
    app.run(host='localhost', port=8080)
