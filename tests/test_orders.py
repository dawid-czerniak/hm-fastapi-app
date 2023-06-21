from fastapi import status
from main import app
from models.order_models import OrderOutput
from utils.utils import get_order_statuses, get_fake_statuses



def test_get_orders(client, test_order_inputs):
    response = client.get("/orders")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(test_order_inputs), f"Not all orders returned"


def test_place_order(client):
    # id will be ignored, and changed on current highest id + 1
    # it has to be provided, otherwise order will not be inserted into db
    # for some reason, adding autoincrement=True to the model does not solve that problem in sqlite
    order_input = {"id": 1, "stoks": "TESTCURR", "quantity": 90}
    response = client.post("/orders", json=order_input)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["confirmation"] == "Order placed"


def test_place_order_with_wrong_quantity_type(client):
    order_input = {"id": 1, "stoks": "TESTCURR", "quantity": "wrong_input12"}
    response = client.post("/orders", json=order_input)
    # FastAPI validates that automatically, and if the type does not match, it will return 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_check_status_of_order_by_id(client, session):
    order_input = {"id": 1, "stoks": "TESTCURR", "quantity": 90}
    response = client.post("/orders", json=order_input)
    response = client.get("/orders/1")

    order_output_status = session.query(OrderOutput).filter(OrderOutput.id == 1).first().status
    assert response.status_code == status.HTTP_200_OK
    # because I assign randomly the status from the list ["PENDING", "EXECUTED", "CANCELLED"]
    # I will assert if returned status is within that list
    assert order_output_status in get_order_statuses(), f"{order_output_status} not in {get_order_statuses}"


def test_check_non_existing_status_of_order_by_id(client, session):
    order_input = {"id": 1, "stoks": "TESTCURR", "quantity": 90}
    response = client.post("/orders", json=order_input)
    response = client.get("/orders/1")

    order_output_status = session.query(OrderOutput).filter(OrderOutput.id == 1).first().status
    assert response.status_code == status.HTTP_200_OK
    # again, because random status assignment, just simulate that given status should not be found in "fake" statuses
    assert order_output_status not in get_fake_statuses(), f"{order_output_status} not in {get_fake_statuses()}"


def test_cancel_order(client, test_order_inputs):
    response = client.delete("/orders/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Item deleted successfully"


def test_cancel_non_existin_order(client, test_order_inputs):
    response = client.delete("/orders/31")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"
