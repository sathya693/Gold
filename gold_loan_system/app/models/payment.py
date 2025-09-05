import enum
from datetime import datetime
from app import db

class PaymentType(str, enum.Enum):
    EMI = 'emi'
    PARTIAL_INTEREST = 'partial_interest'
    PARTIAL_PRINCIPAL = 'partial_principal'
    FULL_CLOSURE = 'full_closure'
    AUCTION_PROCEEDS = 'auction_proceeds'

class PaymentMode(str, enum.Enum):
    CASH = 'cash'
    BANK_TRANSFER = 'bank_transfer'
    UPI = 'upi'
    CHEQUE = 'cheque'
    CARD = 'card'

class Payment(db.Model):
    """
    Model to record all payments made against a loan.
    """
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Payment Details
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    payment_amount = db.Column(db.Numeric(12, 2), nullable=False)
    payment_type = db.Column(db.Enum(PaymentType), nullable=False)
    payment_mode = db.Column(db.Enum(PaymentMode), nullable=False)

    # Allocation
    principal_component = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    interest_component = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)
    penalty_component = db.Column(db.Numeric(12, 2), nullable=False, default=0.0)

    # System and Audit
    received_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Payment {self.receipt_number} for Loan {self.loan_id}>'
