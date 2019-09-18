# FROM https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/#local-migration


from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

# app.config.from_object(os.environ['APP_SETTINGS'])

flask_app = create_app().app

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)


@manager.command
def create_database():
    """
    Create database.
    """
    from database_operations import create_database
    create_database()


manager.add_command('db', MigrateCommand)


@manager.command
def build_database(dataset):
    """
    Populate database with sample dataset.
    """
    from build_database import build_database
    build_database(dataset)


@manager.command
def drop_database():
    """
    Drop database.
    """
    from database_operations import drop_database
    drop_database()


if __name__ == '__main__':
    manager.run()
