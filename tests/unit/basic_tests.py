import os
import unittest
import hamcrest


from context import swappi_app, db_schema

# http://flask.pocoo.org/docs/0.12/testing/


class BasicTests(unittest.TestCase):

    def setUp(self):
        swappi_app.app.config['SQL_DB_URI'] = "sqlite:///db/testitemcatalog.db"
        swappi_app.app.config['TESTING'] = True
        swappi_app.db_init()
        self.app = swappi_app.app.test_client()

    def testIndexContent(self):
        session = swappi_app.get_db_cursor()

        # TODO rewrite test to import all categories from db automatically and check all are present.

        categories = session.query(db_schema.Categories).all()

        categories = [category.name for category in categories]

        response = self.app.get('/')

        for cat in categories:

            hamcrest.assert_that(response.data,
                                 hamcrest.contains_string(cat),
                                 )
