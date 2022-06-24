import click
from flask.cli import with_appcontext
from src.models import User

@click.command(name='fixtures')
@with_appcontext
def fixtures():
    User(name="Isabella").save()
    User(name="Emmanuel").save()
    User(name="Dulcinea").save()
