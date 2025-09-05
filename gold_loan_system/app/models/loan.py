import enum
from datetime import datetime, timedelta
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class InterestCalculationType(str, enum.Enum):
    DAILY = 'daily'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'

class PaymentScheme(str, enum.Enum):
    EMI = 'emi'
    BULLET = 'bullet'
    INTEREST_ONLY = 'interest_only'

class LoanStatus(str, enum.Enum):
    PENDING_APPROVAL = 'pending_approval'
    ACTIVE = 'active'
    CLOSED = 'closed'
    OVERDUE = 'overdue'
    DEFAULTED = 'defaulted'
    AUCTIONED = 'auctioned'

class Loan(db.Model):
    """
    The central Loan model, linking all other components.
    """
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    loan_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Core Loan Terms
    sanctioned_amount = db.Column(db.Numeric(12, 2), nullable=False)
    disbursed_amount = db.Column(db.Numeric(12, 2), nullable=False)
    interest_rate_yearly = db.Column(db.Numeric(5, 2), nullable=False)
    interest_calculation_type = db.Column(db.Enum(InterestCalculationType), nullable=False, default=InterestCalculationType.DAILY)
    payment_scheme = db.Column(db.Enum(PaymentScheme), nullable=False, default=PaymentScheme.BULLET)
    processing_fee = db.Column(db.Numeric(10, 2), default=0.0)

    # Timeline
    loan_start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    loan_duration_days = db.Column(db.Integer, nullable=False)
    actual_closure_date = db.Column(db.Date)

    # EMI Specific
    emi_amount = db.Column(db.Numeric(10, 2))
    next_emi_date = db.Column(db.Date)

    # Status and Flags
    loan_status = db.Column(db.Enum(LoanStatus), nullable=False, default=LoanStatus.PENDING_APPROVAL)
    allows_early_closure = db.Column(db.Boolean, default=True)
    allows_extension = db.Column(db.Boolean, default=False)

    # Financial Tracking
    accumulated_interest = db.Column(db.Numeric(12, 2), default=0.0)
    last_interest_calculation_date = db.Column(db.Date)
    principal_paid = db.Column(db.Numeric(12, 2), default=0.0)
    interest_paid = db.Column(db.Numeric(12, 2), default=0.0)
    penalty_paid = db.Column(db.Numeric(12, 2), default=0.0)

    # System and Audit
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    gold_items = db.relationship('GoldItem', backref='loan', lazy='dynamic', cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='loan', lazy='dynamic', cascade="all, delete-orphan")
    # interest_calculations = db.relationship('InterestCalculation', backref='loan', lazy='dynamic')
    # penalties = db.relationship('Penalty', backref='loan', lazy='dynamic')

    @hybrid_property
    def expected_closure_date(self):
        if self.loan_start_date and self.loan_duration_days:
            return self.loan_start_date + timedelta(days=self.loan_duration_days)
        return None

    @hybrid_property
    def total_due(self):
        return (self.sanctioned_amount - self.principal_paid) + self.accumulated_interest

    def __repr__(self):
        return f'<Loan {self.loan_number}>'
