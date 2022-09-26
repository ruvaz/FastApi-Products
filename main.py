from typing import List

from fastapi import FastAPI, Depends, status, Request, Response, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from Product import schemas, models
from Product.database import engine, SesionLocal

# uvicorn main:app --reload
app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# create tables
models.Base.metadata.create_all(engine)


def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()


# routes for endpoints
# Create product
@app.post('/product', status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# Read all products
@app.get('/products', response_model=List[schemas.DisplayProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products  # return list of products


# Show product by id
@app.get('/product/{id}', response_model=schemas.DisplayProduct)
def get_product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with id {id} not found')
    return product  # return product by id


@app.delete('/product/{id}')
def delete_product(id, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return product


@app.put('/product/{id}')
def update_product(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        return {'message': 'Product not found'}

    product.update(request.dict())
    db.commit()
    return {'message': 'Product updated', 'Product': product.first()}



@app.post('/seller',response_model=schemas.DisplaySeller)
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

