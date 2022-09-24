from datetime import datetime, time, timedelta
from uuid import UUID

from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List  # set not repeat values

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
app = FastAPI()


class Event(BaseModel):
    event_id: UUID
    start_date: datetime
    end_date: datetime  # timestamp
    repeat_time: time  # 00:00:00 timezone
    execute_after: timedelta  # difference between start_date and end_date


class Profile(BaseModel):
    name: str
    age: int
    email: str


class Image(BaseModel):
    url: HttpUrl = Field(..., example="https://example.com/image.jpg")
    name: str = Field(example='Iphone 12', max_length=100)


class Product(BaseModel):
    name: str
    price: float = Field(title='Price of the item',
                         description='This would be price of the item being added', gt=0)
    discount: float
    discounted_price: float
    tags: Set[str] = []  # Sets do not repeat values
    image: List[Image] = []  # list of Images

    class Config:
        schema_extra = {
            'example': {
                'name': 'iPhone 12',
                'price': 1000,
                'discount': 0.1,
                'discounted_price': 900,
                'tags': ['apple', 'phone'],  # set not repeat values
                'image': [
                    {
                        'url': 'https://www.apple.com/v/iphone/home/ab/images/overview/compare/compare_iphone_12__f2x.png',
                        'name': 'iPhone 12'
                    },
                    {
                        'url': 'https://www.apple.com/v/iphone/home/ab/images/overview/compare/compare_iphone_12_pro__f2x.png',
                        'name': 'iPhone 12 Pro'
                    }
                ]
            }
        }


class Offer(BaseModel):
    name: str = Field(..., example='iPhone 12')
    description: str = Field(None, example='iPhone 12 new model')
    price: float = Field(..., example=1100)
    products: List[Product]


class User(BaseModel):
    username: str = Field(..., example='Usuario')
    password: str = Field(..., example='123456')
    email: str = Field(..., example='email@server.com')


@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.post('/addevent')
def add_event(event: Event):
    return event


@app.post('/addoffer')
def add_offer(offer: Offer):
    return offer


@app.post('/adduser')
def add_user(user: User):
    return user


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/ad/{id}")
def about(id: int):
    return {f'message": "About Page {id}'}


@app.get("/movies")
def movies():
    return {'movies': ['movie1', 'movie2']}


@app.get("/user/admin")
def admin():
    return {'username': 'admin'}


@app.get("/user/{username}")
def user(username: str):
    return {f'username': username}


# http://127.0.0.1:8000/products?id=99  Query parameter
@app.get('/products')
def products(id=1, price=10):
    return {f'products': id, 'price': price}


# http://127.0.0.1:8000/products    then use default value 1 and 10
# http://127.0.0.1:8000/products?id=99

# userid path parameter
# commentid query parameter
@app.get('/profile/{userid}/comments')
def profile(userid: int, commentid: int):
    return {f'userid': userid, 'commentid': commentid}


@app.post('/adduser')
def adduser(profile: Profile):
    return {'message': profile}


@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {"product_id": product_id, "product": product, "category": category}
