import click
from flask.cli import with_appcontext
from src.models import Product

@click.command(name='fixtures')
@with_appcontext
def fixtures():
    Product(name="Pants", price=10.5, quantity=10, created_by=1).save()
    Product(name="T-Shirt", price=20.87, quantity=5, created_by=2).save()
    Product(name="XBOX", price=526.61, quantity=21, created_by=3).save()
