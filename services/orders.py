from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from models.order_models import OrderInput, OrderOutput
from sqlalchemy.orm import Session
from utils.utils import random_delay, get_order_statuses
import random


@random_delay
def get_orders(db: Session):
    return db.query(OrderInput).all()


@random_delay
def place_order(order_input: OrderInput, db: Session):
    order_input = OrderInput(stoks=order_input.stoks, quantity=order_input.quantity)
    db.add(order_input)
    db.commit()
    db.refresh(order_input)

    @random_delay
    def create_order_output():
        order_output = OrderOutput(stoks=order_input.stoks, quantity=order_input.quantity, status=random.choice(get_order_statuses()), order_input_id=order_input.id)
        db.add(order_output)
        db.commit()
        db.refresh(order_output)

    create_order_output()
    return {"order_input_id": order_input.id, "confirmation": "Order placed"}


@random_delay
def get_order(order_id: int, db: Session):
    order_input = db.query(OrderInput).filter(OrderInput.id == order_id)
    if not order_input.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    status = db.query(OrderOutput).filter(OrderOutput.id == order_input.first().id).first().status
    return {"stauts": status}


@random_delay
def cancel_order(order_id: int, db: Session):
    order_input = db.query(OrderInput).filter(OrderInput.id == order_id)
    if not order_input.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    order_input.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(content={"detail": "Item deleted successfully"})
