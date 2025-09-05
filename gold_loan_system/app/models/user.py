import enum
from datetime import datetime
from app import db, login
from flask_login import UserMixin
import bcrypt

class UserRoles(str, enum.Enum):
    """Enumeration for user roles to ensure type safety and consistency."""
    ADMIN = 'admin'
    CASHIER = 'cashier'
    CUSTOMER = 'customer'

class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.
    Stores user credentials, roles, and personal information.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRoles), default=UserRoles.CUSTOMER, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships will be fully defined later
    # created_customers = db.relationship('Customer', backref='creator', lazy='dynamic', foreign_keys='Customer.created_by')
    # approved_loans = db.relationship('Loan', backref='approver', lazy='dynamic', foreign_keys='Loan.approved_by')

    def set_password(self, password: str):
        """Hashes the password using bcrypt and stores it."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        if self.password_hash is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'

@login.user_loader
def load_user(user_id: str):
    """Flask-Login callback to load a user from the database by ID."""
    return User.query.get(int(user_id))
