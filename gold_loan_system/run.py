import os
import click
import random
from datetime import date, timedelta
from faker import Faker
from app import create_app, db
from app.models import User, UserRoles, Customer
from flask_migrate import Migrate, upgrade
from sqlalchemy import inspect as sql_inspect

# Create an app instance from the factory
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)


def seed_database_with_initial_data():
    """Seeds the database with initial, realistic demo data."""
    click.echo("Seeding initial data...")
    fake = Faker()

    # Create Admin
    if not User.query.filter_by(username='admin').first():
        click.echo("Creating admin user...")
        admin_user = User(username='admin', full_name='Administrator', email='admin@goldloan.com', phone='0000000000', role=UserRoles.ADMIN, is_active=True)
        admin_user.set_password('Admin@123')
        db.session.add(admin_user)

    # Create Cashiers/Managers
    cashiers = []
    for i in range(1, 3):
        username = f'cashier{i}'
        if not User.query.filter_by(username=username).first():
            click.echo(f"Creating cashier user: {username}...")
            cashier = User(username=username, full_name=f'Cashier {i}', email=f'cashier{i}@goldloan.com', phone=f'111111111{i}', role=UserRoles.CASHIER, is_active=True)
            cashier.set_password('Cashier@123' if i == 1 else 'Cashier@456')
            cashiers.append(cashier)
            db.session.add(cashier)
    db.session.commit() # Commit admin and cashiers to get their IDs

    # Retrieve cashiers from DB to ensure we have their IDs
    cashiers = User.query.filter_by(role=UserRoles.CASHIER).all()
    if not cashiers:
        click.echo("Warning: No cashier accounts found to assign to customers.")
        return

    # Create Customers
    if User.query.filter_by(role=UserRoles.CUSTOMER).count() < 10:
        click.echo("Creating 10 demo customers...")
        for i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}{i}"
            if User.query.filter_by(username=username).first():
                continue # Skip if username somehow already exists

            # Create User record for customer login
            customer_user = User(username=username, full_name=f"{first_name} {last_name}", email=fake.unique.email(), phone=fake.unique.phone_number(), role=UserRoles.CUSTOMER, is_active=True)
            customer_user.set_password('Customer@123')
            db.session.add(customer_user)
            db.session.commit() # Commit to get user ID

            # Create Customer record for KYC details
            customer_details = Customer(
                user_id=customer_user.id,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70),
                gender=random.choice(['Male', 'Female']),
                primary_phone=customer_user.phone,
                email=customer_user.email,
                address_line1=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                pincode=fake.zipcode(),
                created_by=random.choice(cashiers).id
            )
            db.session.add(customer_details)
            db.session.commit()

@app.shell_context_processor
def make_shell_context():
    """Creates a shell context for easier debugging."""
    return {'db': db, 'User': User, 'UserRoles': UserRoles, 'Customer': Customer}

@app.cli.command("seed")
def seed():
    """CLI command to seed the database."""
    with app.app_context():
        seed_database_with_initial_data()
    click.echo("Database seeded.")

def initialize_database():
    """Initializes and seeds the database on first run."""
    with app.app_context():
        inspector = sql_inspect(db.engine)
        if not inspector.has_table('alembic_version'):
            click.echo("Database not initialized. Applying migrations...")
            upgrade()
            seed_database_with_initial_data()
            click.echo("Database setup complete.")

if __name__ == '__main__':
    initialize_database()
    app.run()
