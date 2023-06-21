from fastapi import FastAPI
from api.routers import orders
from db.connection import engine
from models import order_models


order_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(orders.router)
