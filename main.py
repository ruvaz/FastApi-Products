from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

import schemas
import models
from database import engine, get_db
from routers import product, seller, login

# uvicorn main:app --reload

app = FastAPI(
    title='Product API',
    description='This is a simple API for Product',
    version='1.0.0',
    terms_of_service='https://www.google.com/policies/terms/',
    contact={
        'name': 'Ruben',
        'url': 'https://www.google.com',
        'email': 'ruvaz@live.com'
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://www.google.com/policies/terms/'
    },
    openapi_url='/api/openapi.json',
    docs_url='/api/docs',
    redoc_url='/api/redoc'

)

# add product router
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

# create tables
models.Base.metadata.create_all(engine)
