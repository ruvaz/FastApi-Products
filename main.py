from fastapi import FastAPI, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import schemas
import models
from database import engine, get_db
from routers import product

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
    docs_url='/api/documentation',
    redoc_url='/api/redoc'

)

# add product router
app.include_router(product.router)

# to has passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create tables
models.Base.metadata.create_all(engine)


@app.post('/seller', response_model=schemas.DisplaySeller, tags=['Seller'])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashedpassword = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username=request.username,
        email=request.email,
        password=hashedpassword
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
