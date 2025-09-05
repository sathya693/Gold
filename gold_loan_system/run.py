import os
import click
from app import create_app, db
from app.models import User, UserRoles
from flask_migrate import Migrate, upgrade
from sqlalchemy import inspect as sql_inspect

# Create an app instance from the factory
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)


def seed_database_with_initial_data():
    """Seeds the database with initial data."""
    click.echo("Seeding initial data...")
    # Create an admin user
    if not User.query.filter_by(username='admin').first():
        click.echo("Creating admin user...")
        admin_user = User(
            username='admin',
            full_name='Administrator',
            email='admin@goldloan.com',
            phone='0000000000',
            role=UserRoles.ADMIN,  # Use the enum member for the role
            is_active=True
        )
        admin_user.set_password('Admin@123')
        db.session.add(admin_user)
        db.session.commit()
        click.echo("Admin user created.")
    else:
        click.echo("Admin user already exists.")
    # Future seeding for customers, cashiers, etc., can be added here.


@app.shell_context_processor
def make_shell_context():
    """
    Creates a shell context that adds the database instance and core models
    to the shell session, allowing for easier testing and management.
    """
    return {'db': db, 'User': User, 'UserRoles': UserRoles}


@app.cli.command("seed")
def seed():
    """CLI command to seed the database with initial data."""
    seed_database_with_initial_data()


def initialize_database():
    """
    Checks if the database is initialized. If not, it applies all migrations
    and seeds the database with initial data.
    """
    with app.app_context():
        inspector = sql_inspect(db.engine)
        # The 'alembic_version' table is created by Flask-Migrate upon the first migration.
        # Its absence indicates a fresh, uninitialized database.
        if not inspector.has_table('alembic_version'):
            click.echo("Database not initialized. Applying migrations and seeding data...")
            # Apply all pending migrations
            upgrade()
            # Seed the database
            seed_database_with_initial_data()
            click.echo("Database setup complete.")


if __name__ == '__main__':
    # Initialize the database if it's the first run
    initialize_database()
    app.run()
