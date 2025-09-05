from tests.base_test import BaseTestCase
from app.models import User, UserRoles

class TestUserModel(BaseTestCase):

    def test_password_hashing(self):
        """
        Test that password hashing and checking works correctly.
        """
        u = User(username='susan', email='susan@example.com', full_name='Susan Smith', phone='1234567890')
        u.set_password('cat')

        self.assertIsNotNone(u.password_hash)
        self.assertNotEqual(u.password_hash, 'cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_roles(self):
        """
        Test that the user role is set correctly.
        """
        u = User(username='john', role=UserRoles.ADMIN, email='john@example.com', full_name='John Doe', phone='0987654321')
        self.assertEqual(u.role, UserRoles.ADMIN)

    def test_repr(self):
        """
        Test the __repr__ method of the User model.
        """
        u = User(username='testuser', role=UserRoles.CUSTOMER, email='test@test.com', full_name='Test User', phone='1112223333')
        self.assertEqual(repr(u), '<User testuser (customer)>')
