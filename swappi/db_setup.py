from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Base, Categories, Items, Users

engine = create_engine('sqlite:///db/itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_categories = ['spaceships',
                  'drones',
                  'time machines',
                  'Hover Boards',
                  'Jetpacks',
                  ]

for category in new_categories:
    newCategory = Categories(name=category)
    session.add(newCategory)



session.commit()

session = DBSession()

new_spaceships = ['Falcon 10',
                  'Sparrow 2',
                  'Stark 11',
                  ]

for spaceship in new_spaceships:
    newItem = Items(title=spaceship,
                    description='a thing that flies in space',
                    category_id=1,
                    )
    session.add(newItem)

session.commit()