from datetime import datetime
from app import db

class Customer(db.Model):
    """
    Customer model to store personal and KYC information.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)

    # Personal Details
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    marital_status = db.Column(db.String(20))

    # Contact Information
    primary_phone = db.Column(db.String(20), nullable=False, unique=True)
    secondary_phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True) # Optional email

    # Address
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)

    # KYC and ID
    kyc_type = db.Column(db.String(50)) # e.g., Aadhar, PAN, Passport
    kyc_id_number = db.Column(db.String(50), unique=True)
    id_proof_path = db.Column(db.String(255)) # Path to uploaded ID proof image
    photo_path = db.Column(db.String(255)) # Path to uploaded customer photo

    # System Information
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Link to a login account if customer can log in
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Link to the staff who created this customer

    # This defines the one-to-many relationship from Customer to Loan
    loans = db.relationship('Loan', backref='customer', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
