from src.containers import MainContainer
from src.app import User

container = MainContainer()
Session = container.session()

with Session() as session:
    session.add(User(name="Admin"))
    session.add(User(name="Staff"))
    session.add(User(name="User"))
    session.commit()
