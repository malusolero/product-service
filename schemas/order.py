from typing import List
from pydantic import BaseModel

class GetOrderProductSchema(BaseModel):
    """
        Parameters for getting a product inside an order
    """
    id: int = 1
    amount: int = 3
    price: float = 19.99
    product_id: int = 3

class CreateOrderProductSchema(BaseModel):
    """
        Parameters for creating a product inside an order
    """
    amount: int = 3
    price: float = 19.99
    product_id: int = 3


class CreateOrderSchema(BaseModel):
    """
        Parameters for successfully create an order
    """
    user_email: str = 'test@email.com'
    total_price: float = 120.00
    date: str = '2023-09-20T19:15:24.588Z'
    order_products: List[CreateOrderProductSchema] = [
        { "amount": 3, "price": 10.99, "product_id": 1},
        { "amount": 6, "price": 1.99, "product_id": 2 },
        { "amount": 7, "price": 15.99, "product_id": 3 },
   ]

class GetOrderSchema(BaseModel):
    id: int = 1
    total_price: float = 50.99
    user_email: str = 'test@email.com'
    date: str = '2023-09-20T19:15:24.588Z'
    order_products: List[GetOrderProductSchema] = [
        { "amount": 3, "price": 10.99, "product_id": 1 },
        { "amount": 6, "price": 1.99, "product_id": 2 },
        { "amount": 7, "price": 15.99, "product_id": 3  },
   ]

def return_order_products(order_products: List[GetOrderProductSchema]):
    """
        Helper function to format order products
    """
    result = []
    for order_product in order_products:
        result.append({
            "id": order_product.id,
            "amount": order_product.amount,
            "price": order_product.price,
        })

def return_order(order: GetOrderSchema):
    """
        Helper function for returning order content
    """
    print(order)
    return {
        "id": order.id,
        "total_price": order.total_price,
        "user_email": order.user_email,
        "date": order.date,
        "order_products": order.order_products
    }