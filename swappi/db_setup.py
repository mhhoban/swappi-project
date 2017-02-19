from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_schema import Base, Categories, Items, Users


class DbSetup:

    def __init__(self):

        self.db_uri = 'sqlite:///db/itemcatalog.db'

    def db_init(self):

        engine = create_engine(self.db_uri)

        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        session = DBSession()

        # drop any exisitng data
        session.query(Users).delete()
        session.query(Categories).delete()
        session.query(Items).delete()

        session.commit()

        # Create Dummy Users
        session = DBSession()

        new_users = [['John Doe', 'jdoe@mail.thing'],
                     ['Jon Smith', 'smithy@mail.thing'],
                     ]

        for user in new_users:
            newUser = Users(name=user[0],
                            email=user[1],
                            )
            session.add(newUser)

        session.commit()

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
                          'Drake 11',
                          ]

        for spaceship in new_spaceships:
            newItem = Items(title=spaceship,
                            description='a thing that flies in space',
                            category_id=1,
                            poster_id=1,
                            swap_for="a pony"
                            )
            session.add(newItem)

        session.commit()

        session = DBSession()

        new_drones = ['Palantir 1',
                      'Galadriel M',
                      'Shadow V',
                      ]

        for drone in new_drones:
            newItem = Items(title=drone,
                            description='a thing that flies and spies',
                            category_id=2,
                            poster_id=1,
                            swap_for="two ponies"
                            )
            session.add(newItem)

        session.commit()
        session = DBSession()

        new_time_machines = ['Wells IX',
                             'Brown C',
                             'Chrono 3',
                             ]

        for time_machine in new_time_machines:
            newItem = Items(title=time_machine,
                            description='short or long jumps through time',
                            category_id=3,
                            poster_id=1,
                            swap_for="A clarinet."
                            )
            session.add(newItem)

        session.commit()
        session = DBSession()

        new_hover_boards = ['McFly 7',
                            'Biff 0',
                            'Fire B',
                            ]

        for hover_board in new_hover_boards:
            newItem = Items(title=hover_board,
                            description='It floats, when walking is too hard',
                            category_id=4,
                            poster_id=2,
                            swap_for='a Pink Hoverboard'
                            )
            session.add(newItem)

        session.commit()
        session = DBSession()

        new_jetpacks = ['Rocketeer Mark V',
                        'Stark 1',
                        'Branson 9',
                        ]

        for jetpack in new_jetpacks:
            newItem = Items(title=jetpack,
                            description='Basically the coolest thing ever',
                            category_id=5,
                            poster_id=1,
                            swap_for='beesmans gum',
                            )
            session.add(newItem)

        session.commit()
