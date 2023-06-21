from db.connection import get_db
from fastapi import APIRouter, WebSocket, status
from fastapi import Depends
from fastapi.responses import HTMLResponse
from models.order_models import OrderInput, OrderOutput
from schemas import schemas
from services import orders
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from typing import List, Optional
from starlette.exceptions import WebSocketException
from utils import html
import json


router = APIRouter(tags=["orders"])


@router.get("/orders", response_model=Optional[List[schemas.OrderInput]], summary="Retrieve all orders", status_code=status.HTTP_200_OK)
async def get_orders(db: Session=Depends(get_db)):
    return orders.get_orders(db)
    

@router.post("/orders", summary="Place a new order", status_code=status.HTTP_201_CREATED)
async def place_order(order_input: schemas.OrderInput, db: Session=Depends(get_db)):
    return orders.place_order(order_input, db)


@router.get("/orders/{order_id}", summary="Retrieve a specific order", status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db: Session=Depends(get_db)):
    return orders.get_order(order_id, db)


@router.delete("/orders/{order_id}", summary="Cancel an order", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(order_id: int, db: Session=Depends(get_db)):
    return orders.cancel_order(order_id, db)


@router.get("/")
async def get():
    return HTMLResponse(html.html)


connected_clients = set()

@router.get("/ws/orders")
async def ws_orders(db: Session=Depends(get_db)):
    orders = db.query(OrderOutput).all()
    content = ""
    for order in orders:
        content += f"{order.id} - {order.status}<br>"

    return HTMLResponse(html.html_orders.replace("</form>", f"</form><br>{content}"))


@router.websocket("/ws/orders/execute")
async def execute_random_orders(websocket: WebSocket, db: Session=Depends(get_db)):
    await websocket.accept()
    connected_clients.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()

            orders = db.query(OrderOutput).filter(OrderOutput.status != "EXECUTED").order_by(func.random()).limit(10).all()
            updated = {}
            for order in orders:
                order.status = "EXECUTED"
                db.commit()
                updated[order.id] = "EXECUTED"

            await websocket.send_json(updated)
            await notify_order_execution(websocket, updated)

    except WebSocketException as e:
        print(f"Web socket disconnected {e}")
    finally:
        connected_clients.remove(websocket)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session=Depends(get_db)):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            order_input = OrderInput(stoks=data["stoks"], quantity=data["quantity"])
            response = orders.place_order(order_input, db)
            order_output = db.query(OrderOutput).filter(OrderOutput.id == response["order_input_id"]).first()
            data_json = {"id": response["order_input_id"], "stoks": order_input.stoks, "quantity": order_input.quantity, "status": order_output.status}
            
            await websocket.send_json(data_json)
            await notify_order_execution(websocket, data_json)

    except WebSocketException as e:
        print(f"Web socket disconnected {e}")
    finally:
        connected_clients.remove(websocket)


async def notify_order_execution(websocket, data_json):
    for client in connected_clients:
        if websocket != client:
            await client.send_json(data_json)
