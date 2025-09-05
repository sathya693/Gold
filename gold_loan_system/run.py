import os
import click
from app import create_app, db
from app.models.user import User
from flask_migrate import Migrate

# Create an app instance from the factory
config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    Creates a shell context that adds the database instance and core models
    to the shell session, allowing for easier testing and management.
    """
    # This will be expanded as we add more models
    return {'db': db, 'User': User}

@app.cli.command("seed")
def seed():
    """Seeds the database with initial data."""
    click.echo("Seeding database...")
    # Seeding logic will be added here later
    # Example: Create an admin user
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            full_name='Administrator',
            email='admin@goldloan.com',
            phone='0000000000',
            role='ADMIN',
            is_active=True
        )
        admin_user.set_password('Admin@123')
        db.session.add(admin_user)
        db.session.commit()
        click.echo("Admin user created.")
    else:
        click.echo("Admin user already exists.")
    click.echo("Database seeded.")

if __name__ == '__main__':
    app.run()
