import email
import click
from flask.cli import with_appcontext
from src.models import User
from src.config import Config


@click.command(name='fixtures')
@with_appcontext
def fixtures():
    User(name="Admin", email="admin@example.com", password=Config.PASSWORD_TEST_USER).save()
    User(name="staff", email="staff@example.com", password=Config.PASSWORD_TEST_USER).save()
    User(name="user", email="user@example.com", password=Config.PASSWORD_TEST_USER).save()
