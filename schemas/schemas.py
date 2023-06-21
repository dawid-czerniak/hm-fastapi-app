from enum import Enum
from pydantic import BaseModel, validator


class OrderStatus(str, Enum):
    pending = "PENDING"
    executed = "EXECUTED"
    cancelled = "CANCELLED"


class OrderInput(BaseModel):
    id: int
    stoks: str
    quantity: float

    class Config:
        orm_mode = True


class OrderInputShow(OrderInput):
    pass


class OrderOutput(BaseModel):
    id: int
    stoks: str
    quantity: float
    status: OrderStatus

    class Config:
        orm_mode = True
