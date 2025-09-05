from tests.base_test import BaseTestCase
from app.models import User
from app import db

class TestAuthRoutes(BaseTestCase):

    def test_login_page_loads(self):
        """Test that the login page loads correctly."""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

    def test_registration_page_loads(self):
        """Test that the registration page loads correctly."""
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register New Account', response.data)

    def test_user_registration(self):
        """Test that a new user can register."""
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'password': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

    def test_login_and_logout(self):
        """Test user login and logout functionality."""
        # First, create a user to log in with
        user = User(username='loginuser', email='login@example.com', full_name='Login User', phone='1112223333')
        user.set_password('securepassword')
        db.session.add(user)
        db.session.commit()

        # Test login
        response = self.client.post('/auth/login', data={
            'username': 'loginuser',
            'password': 'securepassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'You have been logged in successfully!', response.data)

        # Test logout
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)
        self.assertIn(b'Sign In', response.data) # Should be back on the login page

    def test_protected_route_access(self):
        """Test that protected routes require login."""
        # Try to access dashboard as anonymous user
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data) # Should be redirected to login
        self.assertIn(b'Please log in to access this page.', response.data)

        # Create user and log in
        user = User(username='testuser', email='test@example.com', full_name='Test User', phone='1234567890')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.client.post('/auth/login', data={'username': 'testuser', 'password': 'password123'})

        # Try to access dashboard as logged-in user
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, Test User!', response.data)
