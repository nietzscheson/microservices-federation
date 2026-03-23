from src.containers import MainContainer
from src.app import Product

container = MainContainer()
Session = container.session()

with Session() as session:
    session.add(Product(name="T-Shirt", created_by=1))
    session.add(Product(name="Bag", created_by=1))
    session.add(Product(name="Pants", created_by=1))
    session.commit()
