from db.connection import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship


class OrderInput(Base):
    __tablename__ = "OrderInput"

    id = Column(Integer, primary_key=True, index=True)
    stoks = Column(String)
    quantity = Column(Float)
    order_outputs = relationship("OrderOutput", back_populates="order_input")


class OrderOutput(Base):
    __tablename__ = "OrderOutput"

    id = Column(Integer, primary_key=True, index=True)
    stoks = Column(String)
    quantity = Column(Float)
    status = Column(String, CheckConstraint('status IN ("PENDING", "EXECUTED", "CANCELLED")'))
    order_input_id = Column(Integer, ForeignKey('OrderInput.id'))
    order_input = relationship("OrderInput", back_populates="order_outputs")
