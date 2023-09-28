from model import Base;
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey

class OrderProduct(Base):
    __tablename__= "order-product"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, order_id: int, product_id: int, amount: int, price: int):
        self.order_id = order_id
        self.product_id = product_id
        self.amount = amount
        self.price = price
    
    @staticmethod
    def validate_parmeters(amount: int, price: int):
        if amount < 1: return False
        if price < 0: return False
        return True

    def serialize(self):
        return {"id": self.id,
                "order_id": self.order_id,
                "amount": self.amount,
                "price": self.price}