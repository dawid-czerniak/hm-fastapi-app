import pytest
from db.connection import get_db, Base
from fastapi.testclient import TestClient
from main import app
from models.order_models import OrderInput
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///./testdb.db', connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_order_inputs(session):
    order_inputs = [
        {
            "stoks": "EURUSD",
            "quantity": 1
        },
        {
            "stoks": "EURPLN",
            "quantity": 10,
        },
        {
            "stoks": "USDPLN",
            "quantity": 100,
        },
        {
            "stoks": "PLNUSD",
            "quantity": 1000,
        },
        {
            "stoks": "PLNEUR",
            "quantity": 10000,
        },
        {
            "stoks": "EURCHF",
            "quantity": 100000,
        },
        {
            "stoks": "CHFEUR",
            "quantity": 1000000,
        },
        {
            "stoks": "PLNCHF",
            "quantity": 10000000,
        },
        {
            "stoks": "CHFPLN",
            "quantity": 100000000,
        },
        {
            "stoks": "CHFUSD",
            "quantity": 5
        },
        {
            "stoks": "EURUSD",
            "quantity": 50
        },
        {
            "stoks": "EURPLN",
            "quantity": 500,
        },
        {
            "stoks": "USDPLN",
            "quantity": 5000,
        },
        {
            "stoks": "PLNUSD",
            "quantity": 50000,
        },
        {
            "stoks": "PLNEUR",
            "quantity": 500000,
        },
        {
            "stoks": "EURCHF",
            "quantity": 5000000,

        },
        {
            "stoks": "CHFEUR",
            "quantity": 50000000,
        },
        {
            "stoks": "PLNCHF",
            "quantity": 500000000,
        },
        {
            "stoks": "CHFPLN",
            "quantity": 5000000000,
        },
        {
            "stoks": "CHFUSD",
            "quantity": 50000000000,
        },
        {
            "stoks": "EURUSD",
            "quantity": 9
        },
        {
            "stoks": "EURPLN",
            "quantity": 90,
        },
        {
            "stoks": "USDPLN",
            "quantity": 900,
        },
        {
            "stoks": "PLNUSD",
            "quantity": 9000,
        },
        {
            "stoks": "PLNEUR",
            "quantity": 90000,
        },
        {
            "stoks": "EURCHF",
            "quantity": 900000,
        },
        {
            "stoks": "CHFEUR",
            "quantity": 9000000,
        },
        {
            "stoks": "PLNCHF",
            "quantity": 90000000,
        },
        {
            "stoks": "CHFPLN",
            "quantity": 900000000,
        },
        {
            "stoks": "CHFUSD",
            "quantity": 9000000000,
        },
    ]
    def create_order_input_model(order_input):
        """Function takes a dictionary which will create OrderInput object"""
        return OrderInput(**order_input)
    
    order_map = map(create_order_input_model, order_inputs)
    orders = list(order_map)

    session.add_all(orders)
    session.commit()

    posts = session.query(OrderInput).all()
    return posts
