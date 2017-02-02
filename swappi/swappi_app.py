from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Base, Categories, Items, Users
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def helloWorld():
    return "Shalom, World!"

if __name__ == '__main__':

    app.debug = True
    app.run(host='localhost', port=8080)