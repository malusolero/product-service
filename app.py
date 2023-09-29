from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
import requests

from model import Session, Product, Order, OrderProduct

from schemas import  ErrorSchema, ProductSearchSchema, CreateProductSchema, GetProductResponseSchema, ListProductsSchema, return_product, ProductPathSchema, return_products, CreateOrderSchema, GetOrderSchema, return_order_products

from flask_cors import CORS

SHORTEN_URL_ENDPOINT = 'https://gotiny.cc/api'

info = Info(title="Product Service API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Docs tags
home_tag = Tag(name="Docs", description="Select docs between: Swagger, Redoc or RapiDoc")
product_tag = Tag(name="Product", description="Create, read, update and delete products from database" )
order_tag = Tag(name="Order", description="Create and read orders endpoints.")

def shorten_url(longer_url: str):
    data = {'input': longer_url}
    code =  requests.post(SHORTEN_URL_ENDPOINT, json=data).text.split('code":"')[1].replace('"}]', '')
    return f'https://gotiny.cc/{code}'

@app.get('/', tags=[home_tag])
def home():
    """ Redirects for /openapi, screen for choosing the documentation.
    """
    return redirect('/openapi')

@app.post('/product', tags=[product_tag], responses={"200": GetProductResponseSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_product(body: CreateProductSchema):
    """
        Endpoint for creating a product inside database
    """

    try:
        session = Session()
        

        if not Product.validate_parameters(amount = body.amount, image = body.image, price = body.price):
            error_message = "Pay attention to the required fields. Image must be a valid url, amount and price should have positive values"
            return { "message": error_message},"400"
        
        shortened_image = shorten_url(body.image)
        

        product = Product(name=body.name, description=body.description, amount=body.amount, weight=body.weight, image=shortened_image, price=body.price)
        session.add(product)
        session.flush()
        session.refresh(product)
        session.commit()
        return return_product(product), 201

    except IntegrityError as e:
        error_msg = "Product with received name already exists :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        print(e)
        error_msg = "Error happened when trying to create a new product inside database :/"
        return {"mesage": error_msg}, 400

@app.put('/product/<int:product_id>', tags=[product_tag], responses={"200": GetProductResponseSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_product(body: CreateProductSchema, path: ProductPathSchema ):
    """
        Endpoint for updating a product inside database
    """

    try:
        session = Session()
        

        if not Product.validate_parameters(amount = body.amount, image = body.image, price = body.price):
            error_message = "Pay attention to the required fields. Price must be positive float. Amount must be positive integer. Image must be a valid url."
            return { "message": error_message},"400"

        updated = session.query(Product).filter(Product.id == path.product_id).update({"name":body.name, "description":body.description, "amount":body.amount, "weight":body.weight, "image":body.image, "price":body.price })
        session.commit()
        updated_product = session.query(Product).filter(Product.id == path.product_id).first()
        
        if updated:
            return return_product(updated_product), 200
        else:
            error_msg = 'Product not found in database'
            return {"message": error_msg}, 404
    

    except IntegrityError as e:
        print(e)
        error_msg = "Peoduct with received name already exists :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        print(e)
        error_msg = "Error happened when trying to update a product inside database :/"
        return {"mesage": error_msg}, 400

@app.delete('/product/<int:product_id>', tags=[product_tag], responses={"200": {}, "404": ErrorSchema})
def delete_item(path: ProductPathSchema):
    """ Delete the product for given product name
    """

    session = Session()
    updated = session.query(Product).filter(Product.id == path.product_id).delete()
    session.commit()


    if updated:
        return {}, 200
    else:
        error_msg = 'Product not found in database'
        return {"message": error_msg}, 404

@app.get('/product/<int:product_id>', tags=[product_tag], responses={"200": GetProductResponseSchema, 400: ErrorSchema, 404: ErrorSchema})
def get_product(path: ProductPathSchema):
    """
        Endpoint for getting a product from database with the given id
    """

    try :

        session = Session()
        product = session.query(Product).filter(Product.id == path.product_id).first()

        if not product:
            error_message = 'Product not found'
            return { "message": error_message}, 404

        else:
            return return_product(product), 200
    except:
        error_message= 'Something went wrong'
        return { "message": error_message }

@app.get('/product/', tags=[product_tag], responses={"200": ListProductsSchema, 400: ErrorSchema})
def get_products():
    """
        Endpoint for getting all products from database with the given 
    """

    try :

        session = Session()
        products = session.query(Product).all()

        if not products:
            error_message = 'Product not found'
            return { "products": []}, 200

        else:
            return return_products(products), 200
    except:
        error_message= 'Something went wrong'
        return { "message": error_message }

@app.get('/product/search', tags=[product_tag], responses={"200": ListProductsSchema, "400": ErrorSchema})
def search_product(query: ProductSearchSchema):
    
    try:
        if not query or not query.name:
            return { "products": []}

        name = query.name
        session = Session()
        products = session.query(Product).filter(Product.name.ilike(f'%{name}%')).all()
        
        return return_products(products), 200

    except Exception as e:
        print(e)
        error_message = 'Error happened when searching for a product in database'
        return { "message": error_message}

@app.post("/order", tags=[order_tag], responses={"200": GetOrderSchema, "400": ErrorSchema, "404": ErrorSchema})
def create_order(body: CreateOrderSchema):

    if not Order.validate_parameters(email = body.user_email, total_price=body.total_price):
        error_message = 'Please provide a valid aroguments!'
        return { "message": error_message}, 400

    try:

        session = Session()
        for order_product in body.order_products:
            product = session.query(Product).filter(Product.id == order_product.product_id).first()
            if not product:
                error_message = f'The product with product_id {order_product.product_id} was not found in database.'
                return { "message": error_message }, 404

            if product.amount < order_product.amount:
                error_message = f'The product with product_id {order_product.product_id} has less amount then the ordered amount. Current amount of this product is {product.amount}'
                return { "message" : error_message}, 400
        
        order_request = Order(user_email=body.user_email, total_price=body.total_price, date=body.date)
        session.add(order_request)
        session.flush()
        session.refresh(order_request)
        session.commit()
        
        print('CREATE ORDER ID >>>><')
        print(order_request.id)
        order_products = []
        for op in body.order_products:
            order_product = OrderProduct(amount=op.amount, price=op.price, order_id=order_request.id, product_id=op.product_id)
            print({ "amount": order_product.amount, "price": order_product.price, "order_id": order_product.order_id})
            session.add(order_product)
            session.flush()
            session.refresh(order_product)
            session.commit()
            order_products.append({ "amount": order_product.amount, "price": order_product.price, "order_id": order_product.order_id, "product_id": order_product.product_id})
            print(order_products)
            product = session.query(Product).filter(Product.id == order_product.product_id).first()
            print(product)
            product.amount = product.amount - order_product.amount
            print(product.amount)
            session.query(Product).filter(Product.id == order_product.product_id).update({
                "name": product.name,
                "description": product.description,
                "amount":product.amount,
                "weight":product.weight,
                "image":product.image,
                "price":product.price
            })
            print('DEU MUITO BOM')
            session.commit()


        return ({
            "id": order_request.id,
            "total_price": body.total_price,
            "date": body.date,
            "user_email": body.user_email,
            "order_products": order_products
        }), 200

    except IntegrityError as e:
        error_message = 'Pay atention and submit the request with all the fields valid.'
        print(e)
        return { "message": error_message }, 400
    except Exception as e:
        print(e)
        error_message = 'Error occured when trying to create this order.'
        return { "message": error_message}, 400
    