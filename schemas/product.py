from typing import List
from pydantic import BaseModel, Field

class ProductSearchSchema(BaseModel):
    """ Product will be searched by name
    """
    name: str = Field(example="Detergente", description="Name of the product that you want to search for")

class CreateProductSchema(BaseModel):
    """ Arguments needed for creating a product in the database
    """

    name: str = 'Detergente para mãos'
    description: str = 'Detergente potente para retirar todos os resíduos'
    amount: int = 3
    weight: str = '1L'
    image: str = 'https://example.com'
    price: float = 50.99

class GetProductResponseSchema(BaseModel):
    """ A product should return the product props
    """

    id: int = 1
    name: str = 'Detergente para mãos'
    description: str = 'Detergente potente para retirar todos os resíduos'
    amount: int = 3
    weight: str = '1L'
    image: str = 'https://example.com'
    price: float = 50.99

class ListProductsSchema(BaseModel):
    """ Defines how the list of products should be returned
    """

    items: List[GetProductResponseSchema]

class ProductPathSchema(BaseModel):
    """ Defines the url path product id
    """
    product_id: int = Field(description="Product id")

def return_product(product: GetProductResponseSchema):
    """ Definition of how a product should be returned
    """

    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "amount": product.amount,
        "weight": product.weight,
        "price": product.price,
        "image": product.image,
    }


def return_products(products: List[GetProductResponseSchema]):
    """ Definition of how a list of products should be returned
    """
    result = []
    for product in products:
        result.append(return_product(product))

    return { "products" : result }

