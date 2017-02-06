import hamcrest
import unittest


from context import db_schema, test_db_setup, swappi_app

# http://flask.pocoo.org/docs/0.12/testing/


class BasicTests(unittest.TestCase):

    def setUp(self):
        swappi_app.app.config['SQL_DB_URI'] = "sqlite:///db/testitemcatalog.db"
        swappi_app.app.config['TESTING'] = True

        # new default db for every test
        test_db = test_db_setup.DbSetup(swappi_app.app.config['SQL_DB_URI'])
        test_db.db_init()

        self.app = swappi_app.app.test_client()

    def testIndexContent(self):
        session = swappi_app.get_db_cursor()

        categories = session.query(db_schema.Categories).all()

        categories = [category.name for category in categories]

        response = self.app.get('/')

        for cat in categories:

            hamcrest.assert_that(response.data,
                                 hamcrest.contains_string(cat),
                                 )

    def testContegoryContent(self):

        session = swappi_app.get_db_cursor()

        categories = session.query(db_schema.Categories).all()
        categories = [category.id for category in categories]

        for cat in categories:
            response = self.app.get('/category/'+str(cat))
            items = session.query(db_schema.Items).filter_by(
                category_id=cat).all()

            for item in items:
                hamcrest.assert_that(response.data,
                                     hamcrest.contains_string(item.title))

    def testItemContent(self):

        session = swappi_app.get_db_cursor()

        categories = session.query(db_schema.Categories).all()

        for cat in categories:
            items = session.query(db_schema.Items).filter_by(
                category_id=cat.id).all()

            for item in items:
                response = self.app.get('/item/' + str(item.id))

                hamcrest.assert_that(response.data,
                                     hamcrest.contains_string(cat.name))
                hamcrest.assert_that(response.data,
                                     hamcrest.contains_string(item.title))
                hamcrest.assert_that(response.data,
                                     hamcrest.contains_string(item.description))

    def testNewItemInput(self):

        session = swappi_app.get_db_cursor()

        request = self.app.post('/add-item',
                                data=dict(
                                    item_title='thingy',
                                    item_desc='thingy desc',
                                    item_cat='1',
                                ))

        items = session.query(db_schema.Items).filter_by(
            category_id=1).all()

        item = items[-1]

        self.assertEqual(item.title, 'thingy')
        self.assertEqual(item.description, 'thingy desc')


        # rv = self.app.post('/add', data=dict(
        #     title='<Hello>',
        #     text='<strong>HTML</strong> allowed here'
        # ), follow_redirects=True)

