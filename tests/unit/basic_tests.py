import os
import unittest
import hamcrest

from context import swappi_app

# http://flask.pocoo.org/docs/0.12/testing/


class BasicTests(unittest.TestCase):

    def setUp(self):
        swappi_app.app.config['SQL_DB_URI'] = "sqlite:///db/testitemcatalog.db"
        swappi_app.app.config['TESTING'] = True
        swappi_app.db_init()
        self.app = swappi_app.app.test_client()

    def testIndex(self):
        response = self.app.get('/')
        hamcrest.assert_that(response.data,
                             hamcrest.contains_string('spaceships'),
                             )
