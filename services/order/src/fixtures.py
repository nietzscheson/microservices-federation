from src.containers import MainContainer
from src.app import Order

container = MainContainer()
Session = container.session()

with Session() as session:
    session.add(Order(name="###-001", created_by=1, product=1))
    session.add(Order(name="###-002", created_by=2, product=2))
    session.add(Order(name="###-003", created_by=3, product=3))
    session.commit()
