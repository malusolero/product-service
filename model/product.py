from model import Base
from sqlalchemy import Column, String, Integer, Float
import validators

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(150), nullable=True)
    amount = Column(Integer, nullable=False)
    weight = Column(String(50), nullable=False)
    image = Column(String(150), nullable=True)
    price = Column(Float, nullable=False)

    def __init__(self, name:str, description:str, amount:int, weight:str, image: str, price: float):

        """
        Create a Product model
        Arguments:
            name: product name.
            description: product brand
            amount: quantity of products in the storage
            weight: product weight (in L or Kg or other similar)
            image: product image (must be an image url)
            price: product price
        """

        self.name = name
        self.description = description
        self.amount = amount
        self.weight = weight
        self.image = image
        self.price = price

    @staticmethod
    def validate_parameters(amount: int, image: str, price: int) -> bool:
        if amount < 0: return False
        if price < 0: return False
        return bool(validators.url(image.strip()))


