import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import app as ecom_app


# Define a fixture for the database session
@pytest.fixture(scope='function')
def session():
    # Create an in-memory SQLite database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Teardown: Close the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='session')
def client():
    app = ecom_app.create_app()
    with app.test_client() as client:
        yield client