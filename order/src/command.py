import click
from flask.cli import with_appcontext
from src.models import Order

@click.command(name='fixtures')
@with_appcontext
def fixtures():
    Order(created_by=1).save()
    Order(created_by=1).save()
