from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_schema import Base, Categories, Items, Users


def check_user_exists(session, email):
    """
    Checks whether user is currently registered, returns True if registered, False if not
    :param session:
    :param email:
    :return:
    """
    user = session.query(Users).filter_by(email=email).one()

    if len(user) > 0:
        return True

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

