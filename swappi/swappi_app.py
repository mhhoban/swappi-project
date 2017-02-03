from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Base, Categories, Items, Users
app = Flask(__name__)
app.config['SQL_DB_URI'] = 'sqlite:///db/itemcatalog.db'


engine = create_engine(app.config['SQL_DB_URI'])
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def helloWorld():

    categories = session.query(Categories).all()
    items = session.query(Items).all()

    import pdb
    pdb.set_trace()
    
    a = categories[0]

    return a

if __name__ == '__main__':

    app.debug = True
    app.run(host='localhost', port=8080)