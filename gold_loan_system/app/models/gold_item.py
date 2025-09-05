from datetime import datetime
from app import db

class GoldItem(db.Model):
    """
    Model to store details of each gold item pledged as collateral for a loan.
    """
    __tablename__ = 'gold_items'

    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id'), nullable=False)

    # Item Metadata
    item_type = db.Column(db.String(100), nullable=False)  # e.g., Ring, Chain, Bangle
    item_description = db.Column(db.Text)

    # Weight and Purity
    gross_weight_grams = db.Column(db.Numeric(10, 3), nullable=False)
    stone_weight_grams = db.Column(db.Numeric(10, 3), default=0.0)
    net_weight_grams = db.Column(db.Numeric(10, 3), nullable=False)
    purity_karat = db.Column(db.Integer, nullable=False) # e.g., 22, 24

    # Valuation
    market_rate_per_gram = db.Column(db.Numeric(10, 2), nullable=False)
    appraised_value = db.Column(db.Numeric(12, 2), nullable=False)
    stone_deduction_amount = db.Column(db.Numeric(10, 2), default=0.0)
    final_value = db.Column(db.Numeric(12, 2), nullable=False)

    # Documentation
    image_path = db.Column(db.String(255)) # Path to uploaded item photo

    # System Information
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<GoldItem {self.item_type} ({self.net_weight_grams}g)>'
