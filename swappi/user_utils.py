from db_schema import Items, Users
from sqlalchemy.orm.exc import NoResultFound


def check_user_exists(session, email):
    """
    Checks whether user is currently registered, returns User info
    if registered, False if not
    :param session:
    :param email:
    :return:
    """

    try:
        user = session.query(Users).filter_by(email=email).one()

        user_data = {}

        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email

        return user_data

    except NoResultFound:
        return False


def register_new_user(name, email, session):
    """
    registers a new user if their user data from Google is un-recognized.
    :param name:
    :param email:
    :param session:
    :return:
    """

    newUser = Users(name=name,
                    email=email,
                    )

    session.add(newUser)
    session.commit()


def user_auth_check(login_session):
    """
    checks whether a user is logged in or not.
    :param login_session:
    :return:
    """

    user = {}

    try:
        user['email'] = login_session['user_email']
        user['id'] = login_session['user_id']

    except KeyError:
        user = False

    return user


def user_owner_check(user_data, item_id, session):
    """
    checks whether a user owns, and can thus edit or delete,
    an item.
    :param user_data:
    :param item_id:
    :param session:
    :return:
    """

    if user_data:

        item = session.query(Items).filter_by(id=item_id).one()
        item_owner = item.poster_id

        if item_owner == user_data['id']:
            return True

        else:
            return False

    else:
        return False

