from flask.cli import FlaskGroup

from app import app
from backend import db


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()


"""
    python manage.py create_db
    
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
"""
