from model import Base
from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.orm import relationship
import validators

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_email = Column(String(150), nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(String(100), nullable=False)
    order_products = relationship("OrderProduct")

    def __init__(self, user_email: str, total_price: int, date: DateTime):
        
        """
        Create a Order model
        Arguments:
            user_email: email of the user that creates the order.
            date: order created at
            total_price: order total price
        """
        
        self.user_email = user_email
        self.total_price = total_price
        self.date = date

    @staticmethod
    def validate_parameters(email: str, total_price: int) -> bool:
        if total_price < 0: return False
        return bool(validators.email(email))

    def serialize(self):
        return {"id": self.id,
                "user_email": self.user_email,
                "total_price": self.total_price,
                "date": self.date,
                "order_products": self.order_products}