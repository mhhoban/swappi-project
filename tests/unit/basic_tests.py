import unittest

from context import swappi_app


class BasicTests(unittest.TestCase):

    def testIndex(self):
        a = swappi_app.helloWorld()
        self.assertEqual(a, 'Shalom, World!')
