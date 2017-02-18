from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users


def check_user_exists(session, email):
    """
    Checks whether user is currently registered, returns User info
    if registered, False if not
    :param session:
    :param email:
    :return:
    """

    # TODO re-write as try/except

    user = session.query(Users).filter_by(email=email).all()

    user_data = {}

    if len(user) > 0:
        user = user[0]
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email

        return user_data

    else:
        return False


def register_new_user(name, email, session):

    newUser = Users(name=name,
                    email=email,
                    )

    session.add(newUser)
    session.commit()


def user_auth_check(login_session):

    try:
        user = login_session['user_email']

    except KeyError:
        user = False

    return user

