import unittest
from app import create_app, db

class BaseTestCase(unittest.TestCase):
    """
    A base test case class.
    Sets up the Flask application in testing mode and initializes a clean
    database for each test.
    """
    def setUp(self):
        """
        Called before each test.
        """
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        """
        Called after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
